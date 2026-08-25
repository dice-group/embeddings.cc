#!/usr/bin/env python3
"""List unique URI domains found in an Elasticsearch embedding index."""

import argparse
import csv
import getpass
import os
import re
import sys
from collections import Counter
from urllib.parse import unquote, urlsplit

import requests
import urllib3


DEFAULT_HOST = "https://131.234.29.20:9200"
DEFAULT_INDEX = "global_demo"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Scan embedding entities and write their unique URI domains."
    )
    parser.add_argument("--host", default=DEFAULT_HOST, help="Elasticsearch URL")
    parser.add_argument("--index", default=DEFAULT_INDEX, help="Index to scan")
    parser.add_argument("--user", default="elastic", help="Elasticsearch username")
    parser.add_argument(
        "--password-env",
        default="ELASTIC_PASSWORD",
        help="environment variable containing the password (otherwise prompt)",
    )
    parser.add_argument("--page-size", type=int, default=5000)
    parser.add_argument("--scroll", default="2m", help="scroll context lifetime")
    parser.add_argument(
        "--output",
        default="global_embedding_domains.csv",
        help="output CSV path, or '-' for stdout",
    )
    parser.add_argument(
        "--verify-tls",
        action="store_true",
        help="verify the Elasticsearch TLS certificate (off by default, like curl -k)",
    )
    return parser.parse_args()


def domain_from_entity(entity):
    if not isinstance(entity, str):
        return None

    # Handles values such as "http:%20//iitb.ac.in/" from the current index.
    uri = unquote(entity.strip().strip("<>"))
    uri = re.sub(r"^(https?):\s*//", r"\1://", uri, flags=re.IGNORECASE)

    try:
        parsed = urlsplit(uri)
        domain = parsed.hostname
    except ValueError:
        return None

    if not domain:
        return None
    return domain.rstrip(".").lower()


def scan_domains(session, host, index, page_size, scroll):
    scroll_id = None
    counts = Counter()
    scanned = 0
    invalid = 0

    try:
        response = session.post(
            f"{host.rstrip('/')}/{index}/_search",
            params={"scroll": scroll},
            json={
                "size": page_size,
                "sort": ["_doc"],
                "_source": ["entity"],
                "query": {"match_all": {}},
            },
        )
        response.raise_for_status()
        data = response.json()

        while True:
            scroll_id = data.get("_scroll_id", scroll_id)
            hits = data.get("hits", {}).get("hits", [])
            if not hits:
                break

            for hit in hits:
                entity = hit.get("_source", {}).get("entity")
                domain = domain_from_entity(entity)
                scanned += 1
                if domain:
                    counts[domain] += 1
                else:
                    invalid += 1

            print(
                f"Scanned {scanned:,} embeddings; found {len(counts):,} domains",
                file=sys.stderr,
            )

            response = session.post(
                f"{host.rstrip('/')}/_search/scroll",
                json={"scroll": scroll, "scroll_id": scroll_id},
            )
            response.raise_for_status()
            data = response.json()
    finally:
        if scroll_id:
            try:
                session.delete(
                    f"{host.rstrip('/')}/_search/scroll",
                    json={"scroll_id": [scroll_id]},
                ).raise_for_status()
            except requests.RequestException as exc:
                print(f"Warning: could not clear scroll context: {exc}", file=sys.stderr)

    return counts, scanned, invalid


def write_csv(counts, output_path):
    output = sys.stdout if output_path == "-" else open(
        output_path, "w", encoding="utf-8", newline=""
    )
    try:
        writer = csv.writer(output)
        writer.writerow(["domain", "embedding_count"])
        for domain, count in sorted(counts.items(), key=lambda item: (-item[1], item[0])):
            writer.writerow([domain, count])
    finally:
        if output is not sys.stdout:
            output.close()


def main():
    args = parse_args()
    if args.page_size < 1:
        raise SystemExit("--page-size must be at least 1")

    password = os.environ.get(args.password_env)
    if password is None:
        password = getpass.getpass(f"Password for {args.user}: ")

    if not args.verify_tls:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    with requests.Session() as session:
        session.auth = (args.user, password)
        session.verify = args.verify_tls
        session.headers.update({"Accept": "application/json"})
        counts, scanned, invalid = scan_domains(
            session, args.host, args.index, args.page_size, args.scroll
        )

    write_csv(counts, args.output)
    destination = "stdout" if args.output == "-" else args.output
    print(
        f"Done: {scanned:,} embeddings, {len(counts):,} unique domains, "
        f"{invalid:,} invalid/missing URIs. Wrote {destination}.",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()

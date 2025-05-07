from elasticsearch import helpers

def extract_uris(es_client, index="whale", target=100000, size=1000):
    scan_q = {
        "_source": True,
        "query": {"match_all":{}}
    }

    results = []
    for hit in helpers.scan(
        client=es_client,
        index=index,
        query=scan_q,
        size=size,
        preserve_order=False
    ):
        src = hit.get("_source", {})
        uri = src.get("entity", "")
        if uri and "whale" not in uri.lower():
            results.append(uri)
            if len(results) >= target:
                break

    return results
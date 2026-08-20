import json
import requests

SITE = "http://localhost:1337"
GET_ENTITIES = f"{SITE}/demo/entities"
DEMO_EMB = f"{SITE}/demo/embeddings"

PAGE_SIZE = 100
MAX_URIS = 1000
OUT = "/Users/admin/Coding/embeddings.cc/instance/uris_demo_global.json"

def get_entities(offset):
    r = requests.post(GET_ENTITIES, json={
        "index": "global_demo",
        "size": PAGE_SIZE,
        "offset": offset
    })
    r.raise_for_status()
    data = r.json()
    return data.get("entities", [])

def has_embedding(index, entity):
    r = requests.post(DEMO_EMB, json={"index": index, "entity": entity})
    r.raise_for_status()
    data = r.json()
    return bool(data.get("embeddings"))

found = []
found_set = set()
offset = 0
pages = 0

while len(found) < MAX_URIS:
    pages += 1
    ents = get_entities(offset)
    offset += PAGE_SIZE

    if not ents:
        break

    for e in ents:
        if len(found) >= MAX_URIS:
            break
        if not isinstance(e, str) or not e.startswith("http") or e in found_set:
            continue

        if not has_embedding("local_demo", e):
            continue

        found.append(e)
        found_set.add(e)

    print(f"page {pages}: found={len(found)}")

with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(found, f)

print("Done:", len(found), "saved to", OUT)
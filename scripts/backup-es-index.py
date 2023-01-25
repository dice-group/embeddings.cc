#!/usr/bin/env python3

# Script to backup an Elasticsearch index
# Code is based on the Elasticsearch 8.3 Scroll API
# https://www.elastic.co/guide/en/elasticsearch/reference/8.3/scroll-api.html
# https://elasticsearch-py.readthedocs.io/en/v8.3.1/api.html#elasticsearch.Elasticsearch.scroll
# https://kb.objectrocket.com/elasticsearch/how-to-use-python-to-make-scroll-queries-to-get-all-documents-in-an-elasticsearch-index-752

import sys
from elasticsearch import Elasticsearch
import bz2

# Do not show warning for self-signed certificates
import urllib3
urllib3.disable_warnings()

# Configuration
host = "https://embeddings.cs.upb.de:9200"
user = "elastic"
size = 10*1000
keep_context = "60s"
use_bz2 = True
index = "dbpedia_en_fr_15k_procrustes"
#index = "dbpedia_en_fr_100k_procrustes_v2"
#index = "dbpedia_wikidata_full"

# Get password form CLI
if len(sys.argv) > 1:
    password = sys.argv[1]
else:
    print('Please provide the Elasticsearch user password')
    sys.exit(1)

# Open file
if use_bz2:
    filename_uris = index + '.uris.txt.bz2'
    f_uris = bz2.open(filename_uris, mode='wt', compresslevel=9, encoding=None, errors=None, newline=None)
    filename_emb = index + '.embeddings.txt.bz2'
    f_emb = bz2.open(filename_emb, mode='wt', compresslevel=9, encoding=None, errors=None, newline=None)
else:
    filename_uris = index + '.uris.txt'
    f_uris = open(filename_uris, 'w')
    filename_emb = index + '.embeddings.txt'
    f_emb = open(filename_emb, 'w')
print('Writing to:', filename_uris, filename_emb)

def handle_respose(response):
    print('.', end='', flush=True)
    for doc in response['hits']['hits']:
        f_emb.write(",".join(str(emb) for emb in doc['_source']['embeddings']) + '\n')
        f_uris.write(doc['_source']['entity'] + '\n')

# Default query
client = Elasticsearch(host, http_compress=True, verify_certs=False, basic_auth=(user, password))
match_all = {
    "size": size,
    "query": {
        "match_all": {}
    }
}
response = client.search(
    index = index,
    body = match_all,
    scroll = keep_context
)
handle_respose(response)
scroll_id = response['_scroll_id']

# Request until no further results available
while len(response['hits']['hits']):
    response = client.scroll(
        scroll_id = scroll_id,
        scroll = keep_context
    )
    handle_respose(response)
    scroll_id = response['_scroll_id']

# Finally close file
f_uris.close()
f_emb.close()

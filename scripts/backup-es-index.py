#!/usr/bin/env python3

# Script to backup an Elasticsearch index
# Code is based on the Elasticsearch 8.3 Scroll API
# https://www.elastic.co/guide/en/elasticsearch/reference/8.3/scroll-api.html
# https://elasticsearch-py.readthedocs.io/en/v8.3.1/api.html#elasticsearch.Elasticsearch.scroll
# https://kb.objectrocket.com/elasticsearch/how-to-use-python-to-make-scroll-queries-to-get-all-documents-in-an-elasticsearch-index-752

import sys
from elasticsearch import Elasticsearch
import urllib3
urllib3.disable_warnings() # Do not show warning for self-signed certificates
sys.path.insert(1, '../api/serialization/')
from file_writer import FileWriter


# Configuration
host = "https://embeddings.cs.upb.de:9200"
user = "elastic"
size = 10 * 1000
keep_context = "60s"
file_format = FileWriter.FORMAT_BZIP2  # FORMAT_BZIP2 or FORMAT_TEXT


# Get password form CLI
if len(sys.argv) > 1:
    password = sys.argv[1]
else:
    print('Please provide the Elasticsearch user password')
    sys.exit(1)

# Get index form CLI
if len(sys.argv) > 2:
    index = sys.argv[2]
else:
    print('Please provide the Elasticsearch index to backup')
    sys.exit(1)


# Writing
writer = FileWriter(id=index, format=file_format)
writer.open()

def handle_respose(response, file_writer):
    print('.', end='', flush=True)
    for doc in response['hits']['hits']:
        writer.add(doc['_source']['entity'], doc['_source']['embeddings'])


# Default query and first request
client = Elasticsearch(host, http_compress=True, verify_certs=False, basic_auth=(user, password))
match_all = {
    "size": size,
    "query": {
        "match_all": {}
    }
}
response = client.search(
    index=index,
    body=match_all,
    scroll=keep_context
)
handle_respose(response, writer)
scroll_id = response['_scroll_id']

# Request until no further results available
while len(response['hits']['hits']):
    response = client.scroll(
        scroll_id=scroll_id,
        scroll=keep_context
    )
    handle_respose(response, writer)
    scroll_id = response['_scroll_id']

# Finally close files
writer.close()
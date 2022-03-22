# embeddings.cc create logging index
# https://github.com/dice-group/embeddings.cc
#
# https://www.elastic.co/guide/en/elasticsearch/reference/7.16/mapping-types.html
# https://www.elastic.co/guide/en/elasticsearch/reference/7.16/date.html
# https://www.elastic.co/guide/en/elasticsearch/reference/7.16/ip.html
# https://www.elastic.co/guide/en/elasticsearch/reference/7.16/flattened.html
#
# Usage:       python3 scripts/create-logger.py <PASSWORD>
# Local usage: python3 scripts/create-logger.py <PASSWORD> http://127.0.0.1:8008
import sys
from elasticsearch import Elasticsearch

es_host = 'http://localhost:9200'
es_user = 'elastic'
es_password = None
es_index = 'usagelog'

do_delete_index = False
do_create_index = False
do_print_indexes = False
do_add_data = False
do_count = False
do_search = False

# Get password form CLI
if len(sys.argv) > 1:
    es_password = sys.argv[1]
else:
    print('Please provide a password')
    sys.exit(1)

# Get webservice URL form CLI
webservice_url = None
if len(sys.argv) > 2:
    es_host = sys.argv[2]

# Create ES instance
es = Elasticsearch(es_host, http_compress=True, http_auth=(es_user, es_password))

# Delete index
if do_delete_index:
    es.indices.delete(es_index)

# Create index
if do_create_index:
    index_config = {
        'settings': {
            'number_of_shards': 2,
            'number_of_replicas': 1
        },
        'mappings': {
            'properties': {
                "date": {
                    "type": "date",
                    "format": "epoch_second"
                },
                "ip": {
                    "type": "keyword"
                },
                'path': {
                    'type': 'keyword'
                },
                'parameters': {
                    'type': 'flattened'
                }
            }
        }
    }
    es.indices.create(index=es_index, body=index_config)

# Print indexes
if do_print_indexes:
    for index in es.indices.get_alias("*"):
        print('->', index)

import hashlib
import ipaddress


def get_ip_hashes():
    ipv4 = socket.gethostbyname(socket.gethostname())
    ipv6 = ipaddress.IPv6Address('2002::' + ipv4).exploded
    hashes = []
    for part in ipv6.split(':'):
        hashes.append(hashlib.shake_256(part.encode()).hexdigest(1))
    return hashes[:-1]


# Example data
# IP has to come from webserver user
import socket
import time

# Add data
if do_add_data:
    ip = get_ip_hashes()
    time = int(time.time())
    path = '/api/test/log/me'
    params = {'size': 100, 'offset': 0}

    es.index(es_index, body={
        'date': time,
        'ip': ip,
        'path': path,
        'parameters': params
    })

# Count docs
if do_count:
    print('count:', es.count(index=es_index))

# Get docs
if do_search:
    print('search:', es.search(index=es_index, body={"query": {"match_all": {}}})['hits']['hits'])
    print('search 2:', es.search(index=es_index, body={"query": {"term": {"parameters": 100}}})['hits']['hits'])
    print('search 3:', es.search(index=es_index, body={"query": {"term": {"parameters.size": 100}}})['hits']['hits'])
    # print('search offset:', es.search(index=es_index, body={"from": 0, "size": 5, "query": {"match_all": {}}})['hits']['hits'])

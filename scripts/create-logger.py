import sys
from elasticsearch import Elasticsearch

es_host = 'http://localhost:9200'
es_user = 'elastic'
es_password = None
es_index = 'logger'

do_delete_index = False
do_create_index = False
do_print_indexes = False
do_add_data = False

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
    # https://www.elastic.co/guide/en/elasticsearch/reference/7.16/mapping-types.html
    # https://www.elastic.co/guide/en/elasticsearch/reference/7.16/date.html
    # https://www.elastic.co/guide/en/elasticsearch/reference/7.16/ip.html
    # https://www.elastic.co/guide/en/elasticsearch/reference/7.16/array.html
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
                    "type": "ip"
                },
                'path': {
                    'type': 'keyword'
                },
                'parameters': {
                    'type': 'keyword'
                }
            }
        }
    }
    es.indices.create(es_index, body=index_config)

# Print indexes
if do_print_indexes:
    for index in es.indices.get_alias("*"):
        print('->', index)

# Example data
# IP has to come from webserver user
import socket
import time

ip = socket.gethostbyname(socket.gethostname())
time = int(time.time())
path = '/api/test/log/me'
params = [['size', 100], ['offset', 0]]

# Add data
if do_add_data:
    es.index(es_index, body={
        'date': time,
        'ip': ip,
        'path': path,
        'parameters': params
    })

# Count docs
print(es.count(index=es_index))

# Get docs
print(es.search(index=es_index, body={"query": {"match_all": {}}})['hits']['hits'])

# State: Works. Check filter of parameters
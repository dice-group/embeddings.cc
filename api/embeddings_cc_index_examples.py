# Examples for embeddings.cc index API
# https://github.com/dice-group/embeddings.cc
#
# Usage:       python3 api/embeddings_cc_index_examples.py <PASSWORD>
# Local usage: python3 api/embeddings_cc_index_examples.py <PASSWORD> http://127.0.0.1:8008

import sys
from embeddings_cc_index import EmbeddingsCcIndex

# Configuration
es_index = 'index_test'
#es_index = 'openea_v1.1_dbpedia_en_fr_100k_v1_shallom_10_300___'

# Get password form CLI
if len(sys.argv) > 1:
    password = sys.argv[1]
else:
    print('Please provide a password')
    sys.exit(1)

# Get webservice URL form CLI
webservice_url = None
if len(sys.argv) > 2:
    webservice_url = sys.argv[2]

# Create instance
embeddings_cc_index = EmbeddingsCcIndex(webservice_url=webservice_url)

print("es_index:", es_index)
print("webservice_url:", webservice_url)

# ----------| GET requests without password |---------------------------------------------------------------------------

# Ping webservice
if True:
    statusCode = embeddings_cc_index.ping(seconds=1)
    if statusCode == 502:
        print('502: Webservice unavailable')
        sys.exit(1)
    elif statusCode == 503:
        print('503: Elasticsearch service unavailable')
        sys.exit(1)
    else:
        print(statusCode)

# Returns number of documents in Elasticsearch index.
if False:
    response = embeddings_cc_index.count(es_index)
    print(response.status_code, response.text)

# Searches for an entity in Elasticsearch and returns related embeddings.
if False:
    response = embeddings_cc_index.get_embeddings(es_index, 'http://example.com/0')
    print(response.status_code, response.text)

# ----------| POST requests with password |-----------------------------------------------------------------------------

# Returns webservice response containing existing Elasticsearch indexes.
if True:
    response = embeddings_cc_index.get_indexes(password)
    print(response.status_code, response.text)

# Creates an Elasticsearch index and returns Elasticsearch API response.
if False:
    response = embeddings_cc_index.create_index(password, es_index, 10, shards=5)
    print(response.status_code, response.text)

# Deletes an Elasticsearch index and returns Elasticsearch API response.
if False:
    response = embeddings_cc_index.delete_index(password, es_index)
    print(response.status_code, response.text)

# Adds data.
# Data is transformed to JSON, so tuples and lists are handled equally.
# Important: Split your data into multiple requests and wait for a response
# before adding additional data. A request can take max 50,000 items.
# Also important: Ensure the embeddings are in numeric format (not string).
if False:
    embeddings = [('http://example.com/0', [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]),
                  ('http://example.com/1', [1, 2, 3, 4, 5, 6, 7, 8, 9, 0])]
    print(embeddings)
    response = embeddings_cc_index.add(password, es_index, embeddings)
    print(response.status_code, response.text)
if False:
    embeddings = [['http://example.com/2', [2, 3, 4, 5, 6, 7, 8, 9, 0, 1]],
                  ['http://example.com/3', [3, 4, 5, 6, 7, 8, 9, 0, 1, 2]]]
    print(embeddings)
    response = embeddings_cc_index.add(password, es_index, embeddings)
    print(response.status_code, response.text)
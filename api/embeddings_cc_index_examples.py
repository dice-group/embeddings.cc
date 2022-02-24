# Examples for embeddings.cc index API
# https://github.com/dice-group/embeddings.cc
#
# For local tests use: python3 api/embeddings_cc_index_examples.py <PASSWORD> http://127.0.0.1:8008

import sys
from embeddings_cc_index import EmbeddingsCcIndex

# Get password and webservice URL form CLI
webservice_url = None
if len(sys.argv) > 2:
    webservice_url = sys.argv[2]
if len(sys.argv) > 1:
    password = sys.argv[1]
else:
    print('Please provide a password')
    sys.exit(1)

# Create instance
embeddings_cc_index = EmbeddingsCcIndex(webservice_url=webservice_url)

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

# Returns webservice response containing existing Elasticsearch indexes.
if True:
    response = embeddings_cc_index.get_indexes(password)
    print(response.status_code, response.text)

# Creates an Elasticsearch index and returns Elasticsearch API response.
if False:
    response = embeddings_cc_index.create_index(password, 'index_test', 10, number_of_shards=5)
    print(response.status_code, response.text)

# Deletes an Elasticsearch index and returns Elasticsearch API response.
if False:
    response = embeddings_cc_index.delete_index(password, 'index_test')
    print(response.status_code, response.text)

# Adds embeddings.
# Data is transformed to JSON, so tuples and lists are handled equally.
# Important: Split your data into multiple requests and wait for a response
# before adding additional data. A request can take max 50,000 items.
if False:
    embeddings = [('http://example.com/0', [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]),
                  ('http://example.com/1', [1, 2, 3, 4, 5, 6, 7, 8, 9, 0])]
    response = embeddings_cc_index.add(password, 'index_test', embeddings)
    print(response.status_code, response.text)
if False:
    embeddings = [['http://example.com/2', [2, 3, 4, 5, 6, 7, 8, 9, 0, 1]],
                  ['http://example.com/3', [3, 4, 5, 6, 7, 8, 9, 0, 1, 2]]]
    response = embeddings_cc_index.add(password, 'index_test', embeddings)
    print(response.status_code, response.text)

# Searches for an entity in Elasticsearch and returns related embeddings.
if False:
    response = embeddings_cc_index.get_embeddings('index_test', 'http://example.com/0')
    print(response.status_code, response.text)
# Examples for embeddings.cc index API
# https://github.com/dice-group/embeddings.cc

import sys
from embeddings_cc_index import EmbeddingsCcIndex

# Get password form CLI
if len(sys.argv) > 1:
    password = sys.argv[1]

# Create instance
embeddings_cc_index = EmbeddingsCcIndex(webservice_url='http://127.0.0.1:5000/')

# Returns true, if status code 200 is returned
if False:
    response = embeddings_cc_index.ping(seconds=1)
    print(type(response), response)

# Returns existing indexes
if False:
    response = embeddings_cc_index.get_indexes(password)
    print(response.status_code, response.text)

# Creates an index
if False:
    response = embeddings_cc_index.create_index(password, 'index_test', 10, number_of_shards=5)
    print(response.status_code, response.text)

# Deletes an index
if False:
    response = embeddings_cc_index.delete_index(password, 'index_test')
    print(response.status_code, response.text)

# Adds embeddings
# Data is transformed to JSON, so tuples and lists are handled equally.
# Important: Split your data into multiple requests and wait for a response
# before adding additional data. A request could take e.g. 50,000 items.
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

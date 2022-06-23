# Examples for embeddings.cc index API
# https://github.com/dice-group/embeddings.cc
#
# Usage:       python3 api/embeddings_cc_index_examples.py <PASSWORD>
# Local usage: python3 api/embeddings_cc_index_examples.py <PASSWORD> http://127.0.0.1:8008

import sys
from embeddings_cc_index import EmbeddingsCcIndex

# Configuration
es_index = 'index_test'
es_alias = 'index_test_alias'
es_dimensions = 10
es_shards = 5
#
#es_index = 'dbp_en_de_100k'
#es_alias = 'dbp-en-de-100k'
#es_dimensions = 300
#
#es_index = 'dbp_en_fr_100k'
#es_alias = 'dbp-en-fr-100k'
#es_dimensions = 300
#
#es_index = 'dbp_en_fr_15k'
#es_alias = 'dbp-en-fr-15k'
#es_dimensions = 300

# Execution
do_ping           = True
do_delete_index   = False
do_create_index   = False
do_alias_delete   = False
do_alias_put      = False
do_print_indexes  = True
do_add_data_tuple = False
do_add_data_list  = False
do_count          = False
do_search         = False

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

# Print configuration
print("es_index:", es_index)
print("es_dimensions:", es_dimensions)
print("webservice_url:", webservice_url)

# Create instance
embeddings_cc_index = EmbeddingsCcIndex(webservice_url=webservice_url)

# ----------| PING request without password |---------------------------------------------------------------------------

# Ping webservice
if do_ping:
    statusCode = embeddings_cc_index.ping(seconds=1)
    if statusCode == 502:
        print('502: Webservice unavailable (Check VPN)')
        sys.exit(1)
    elif statusCode == 503:
        print('503: Elasticsearch service unavailable')
        sys.exit(1)
    else:
        print('ping:', statusCode)

# ----------| POST requests with password |-----------------------------------------------------------------------------

# Deletes an Elasticsearch index and returns Elasticsearch API response.
if do_delete_index:
    response = embeddings_cc_index.delete_index(password, es_index)
    print('delete_index:', response.status_code, response.text)

# Creates an Elasticsearch index and returns Elasticsearch API response.
if do_create_index:
    response = embeddings_cc_index.create_index(password, es_index, es_dimensions, shards=es_shards)
    print('create_index:', response.status_code, response.text)

# Deletes an alias of an index.
if do_alias_delete:
    response = embeddings_cc_index.alias_delete(password, es_index, es_alias)
    print('alias_delete:', response.status_code, response.text)

# Adds an alias for an index.
if do_alias_put:
    response = embeddings_cc_index.alias_put(password, es_index, es_alias)
    print('alias_put:', response.status_code, response.text)

# Returns webservice response containing existing Elasticsearch indexes.
if do_print_indexes:
    response = embeddings_cc_index.get_indexes(password)
    print('get_indexes:', response.status_code, response.text)

# Adds data.
# Data is transformed to JSON, so tuples and lists are handled equally.
# Important: Split your data into multiple requests and wait for a response
# before adding additional data. A request can take max 50,000 items.
# Also important: Ensure the embeddings are in numeric format (not string).
if do_add_data_tuple:
    embeddings = [('http://example.com/0', [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]),
                  ('http://example.com/1', [1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9, 0.0])]
    print(embeddings)
    response = embeddings_cc_index.add(password, es_index, embeddings)
    print('add tuple:', response.status_code, response.text)

# Note: Adds two embeddings for same entity
if do_add_data_list:
    embeddings = [['http://example.com/A_similarity_test', [2, 3, 4, 5, 6, 7, 8, 9, 0, 1]],
                  ['http://example.com/Another_similarity_test', [3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9, 0.0, 1.1, 2.2]]]
    print(embeddings)
    response = embeddings_cc_index.add(password, es_index, embeddings)
    print('add list:', response.status_code, response.text)

# ----------| GET requests without password |---------------------------------------------------------------------------

# Returns number of documents in Elasticsearch index.
if do_count:
    response = embeddings_cc_index.count(es_index)
    print('count [status, time, time, count]:', response.status_code, response.text)

# Searches for an entity in Elasticsearch and returns related embeddings.
if do_search:
    response = embeddings_cc_index.get_embeddings(es_index, 'http://example.com/2')
    print('get_embeddings:', response.status_code, response.text)

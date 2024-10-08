# Examples for embeddings.cc index API
# https://github.com/dice-group/embeddings.cc
#
# Usage:       python3 api/embeddings_cc_index_examples.py <PASSWORD>
# Local usage: python3 api/embeddings_cc_index_examples.py <PASSWORD> http://127.0.0.1:8008

import sys
import pandas as pd
from embeddings_cc_index import EmbeddingsCcIndex

# Configuration
es_index      = 'index_vicodi'
es_alias      = 'index_vicodi_alias'
es_dimensions = 40
es_shards     = 5

# Execution
do_ping                  = True
do_print_cpu_usage       = False
do_delete_index          = True
do_create_index          = True
do_create_index_usagelog = True
do_alias_delete          = False
do_alias_put             = True
do_add_data              = True
do_print_indexes         = True
do_count                 = False
do_search                = False



def add_embeddings(api, password, index, embeddings, i):
    response = api.add(password, index, embeddings)
    if response.status_code == 200:
        print(i, end=' ')
        sys.stdout.flush()
        return True
    else:
        print('Could not add embeddings', response.status_code, response.text)
        return False

# Get password from CLI
if len(sys.argv) > 1:
    password = sys.argv[1]
else:
    print('Please provide a password')
    sys.exit(1)

# Get webservice URL form CLI
webservice_url = None
if len(sys.argv) > 2:
    webservice_url = sys.argv[2]
    
embeddings_path = None
if len(sys.argv) > 3:
    embeddings_path = sys.argv[3]

# Print configuration
print("es_index:",       es_index)
print("es_alias:",       es_alias)
print("es_dimensions:",  es_dimensions)
print("es_shards:",      es_shards)
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

# Creates the Elasticsearch index 'usagelog' and returns Elasticsearch API response.
if do_create_index_usagelog:
    response = embeddings_cc_index.create_index_usagelog(password)
    print('create_index_usagelog:', response.status_code, response.text)

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



if do_add_data:
    try:
        data = pd.read_csv(embeddings_path, index_col=0)
    except:
        print(f"Cannot find file {embeddings_path}")
        sys.exit(1)
    embeddings = [(name, data.loc[name].values.tolist()) for name in data.index]
    print("\nTotal number of entities: ", len(embeddings),"\n")
    Embeddings = []
    for i in range(0, len(embeddings), 5000):
    	Embeddings = embeddings[i:i+5000]
    	if not add_embeddings(embeddings_cc_index, password, es_index, Embeddings, min(i+5000, len(embeddings))):
            break

# Gets the maximum CPU useage of ES nodes
if do_print_cpu_usage:
    response = embeddings_cc_index.get_max_cpu_usage(password)
    print('cpu usage:', response.status_code, response.text)

# ----------| GET requests without password |---------------------------------------------------------------------------

# Returns number of documents in Elasticsearch index.
if do_count:
    response = embeddings_cc_index.count(es_index)
    print('count [status, time, time, count]:', response.status_code, response.text)

# Searches for an entity in Elasticsearch and returns related embeddings.
if do_search:
    response = embeddings_cc_index.get_embeddings(es_index, 'http://example.com/2')
    print('get_embeddings:', response.status_code, response.text)

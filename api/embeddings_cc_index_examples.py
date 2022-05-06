# Examples for embeddings.cc index API
# https://github.com/dice-group/embeddings.cc
#
# Usage:       python3 api/embeddings_cc_index_examples.py <PASSWORD>
# Local usage: python3 api/embeddings_cc_index_examples.py <PASSWORD> http://127.0.0.1:8008

import sys
import ast
from embeddings_cc_index import EmbeddingsCcIndex
import numpy as np
import json
import os

# Configuration
<<<<<<< Updated upstream
es_index = 'index_test'
es_alias = 'index_test_alias'
es_dimensions = 10
es_shards = 5
#
#es_index = 'caligraph_dbpedia_procrustes'
#es_alias = 'caligraph-dbpedia-procrustes'
#es_dimensions = 200
#
#es_index = 'caligraph_dbpedia_procrustes_40shards'
#es_dimensions = 200
#es_shards = 40

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
=======
#es_index = 'caligraph_dbpedia_procrustes'
#es_index = 'dbpedia_en_fr_15k_procrustes'
es_index = 'dbpedia_en_fr_100k_procrustes'
#es_index = 'dbpedia_en_fr_15k_v2_shallom___'
#es_index = 'dbpedia_en_fr_100k_v2_v_1-1_shallom___'
>>>>>>> Stashed changes

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

<<<<<<< Updated upstream
# Print configuration
print("es_index:", es_index)
print("es_dimensions:", es_dimensions)
print("webservice_url:", webservice_url)

# Create instance
embeddings_cc_index = EmbeddingsCcIndex(webservice_url=webservice_url)

# ----------| PING request without password |---------------------------------------------------------------------------
=======
# Create instance
embeddings_cc_index = EmbeddingsCcIndex(webservice_url=webservice_url)

# ----------| GET requests without password |---------------------------------------------------------------------------
>>>>>>> Stashed changes

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
<<<<<<< Updated upstream
        print('ping:', statusCode)

# ----------| POST requests with password |-----------------------------------------------------------------------------

# Deletes an Elasticsearch index and returns Elasticsearch API response.
if do_delete_index:
    response = embeddings_cc_index.delete_index(password, es_index)
    print('delete_index:', response.status_code, response.text)
=======
        print(statusCode)
        
    #response = embeddings_cc_index.count(es_index)
    #print('Counting entities: ')
    #print(response.status_code, response.text)

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
if False:
    response = embeddings_cc_index.get_indexes(password)
    print(response.status_code, response.text)
>>>>>>> Stashed changes

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
<<<<<<< Updated upstream
# Also important: Ensure the embeddings are in numeric format (not string).
if do_add_data_tuple:
=======
if False:
>>>>>>> Stashed changes
    embeddings = [('http://example.com/0', [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]),
                  ('http://example.com/1', [1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9, 0.0])]
    print(embeddings)
    response = embeddings_cc_index.add(password, es_index, embeddings)
    print('add tuple:', response.status_code, response.text)

# Note: Adds two embeddings for same entity
if do_add_data_list:
    embeddings = [['http://example.com/2', [2, 3, 4, 5, 6, 7, 8, 9, 0, 1]],
                  ['http://example.com/2', [3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9, 0.0, 1.1, 2.2]]]
    print(embeddings)
    response = embeddings_cc_index.add(password, es_index, embeddings)
<<<<<<< Updated upstream
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
=======
    print(response.status_code, response.text)
if True:
# Add data of a CSV file
#
# Data: https://hobbitdata.informatik.uni-leipzig.de/KGE/DBpedia_EN_FR_15K/V2/Shallom.zip
# Line format: http://dbpedia.org/resource/E734345,0.4001125,[...],-0.015108802
#
# Note: Adding 1,000 embeddings takes around 15 seconds
# time python3 api/embeddings_cc_index_examples.py <PASSWORD>                -> 7m47,509s (Reading/parsing: ~33s)
# time python3 api/embeddings_cc_index_examples.py 123 http://1embeddingsa_EN_FR_100K_V2/Shallom_entity_embeddings.csv'
    max_docs = 100 * 1000
    dimensions = 300

    print('Strating...\n')
    # Delete index
    response = embeddings_cc_index.delete_index(password, es_index)
    print(response.status_code, response.text)

    # Create index
    response = embeddings_cc_index.create_index(password, es_index, dimensions, shards=5)
    print(response.status_code, response.text)

    # Add data
    def add_embeddings(api, password, index, embeddings):
        response = api.add(password, index, embeddings)
        if response.status_code == 200:
            print(i, end=' ')
            sys.stdout.flush()
            return True
        else:
            print(response.status_code, response.text)
            return False

    base_path = os.path.dirname(os.path.realpath(__file__))
    file_path = base_path.split('embeddings.cc')[0]+'Shallom_EnFr_100K_V1/'
    print('\nLoading embeddings...\n')
    with open(file_path+'list_merged_entities_db_fr_en.txt') as file:
        entities = file.read().split('\t')
    with open(file_path+'english2french.json') as file:
        alignment = json.load(file)
    embeddings = np.load(file_path+'/Universal_Emb.npy')
    print('Done!\n')
    Embeddings = []
    print("\nDimensions:", embeddings.shape[1])
    print()
    assert len(entities) == embeddings.shape[0], f"{len(entities)}, {embeddings.shape[0]}"
    for i, ent in enumerate(entities):
        Embeddings.append([ent, list(embeddings[i])])
        if ent in alignment:
            Embeddings.append([alignment[ent], list(embeddings[i])])

        if i % 5000 == 0:
            if not add_embeddings(embeddings_cc_index, password, es_index, Embeddings):
                break
            Embeddings = []
    if len(Embeddings) > 0:
        add_embeddings(embeddings_cc_index, password, es_index, Embeddings)
    # Print number of documents
    response = embeddings_cc_index.count(es_index)
    print(response.status_code, response.text)
>>>>>>> Stashed changes

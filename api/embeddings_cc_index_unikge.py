# UniKGE/Procrustes & embeddings.cc index API
# https://github.com/dice-group/embeddings.cc
#
# Usage:       time python3 api/embeddings_cc_index_unikge.py <PASSWORD>
# Local usage: time python3 api/embeddings_cc_index_unikge.py <PASSWORD> http://127.0.0.1:8008
#
# Runtime local: 21m59,087s (incl. 3x3min sleep time)
# Authors (for questions): N'Dah Jean Kouagou, Adrian Wilke
#
# Note: To be available via the API, create the following aliases afterwards:
# Index                            Alias
# dbpedia_en_fr_15k_procrustes     dbpedia-en-fr-15k
# dbpedia_en_fr_100k_procrustes_v2 dbpedia-en-fr-100k
# dbpedia_en_de_100k_procrustes    dbpedia-en-de-100k
# dbpedia_caligraph_procrustes     dbpedia-caligraph

import sys
import numpy as np
import json
import time
from embeddings_cc_index import EmbeddingsCcIndex

# Configuration
# UniKGE/Procrustes data: https://hobbitdata.informatik.uni-leipzig.de/UniKGE/
es_indices = [
    "dbpedia_en_fr_15k_procrustes",
    "dbpedia_en_fr_100k_procrustes_v2",
    "dbpedia_en_de_100k_procrustes",
    "dbpedia_caligraph_procrustes"
]
# Each folder has to contain: alignment.json, list_merged_entities.txt, Universal_Emb.npy
# Do not forget final '/'
data_folders = [
    "/home/wilke/Data/UniKGE/dbpedia_en_fr_15k_procrustes/EnFr15KV1/",
    "/home/wilke/Data/UniKGE/dbpedia_en_fr_100k_procrustes/EnFr100KV2/",
    "/home/wilke/Data/UniKGE/dbpedia_en_de_100k_procrustes/EnDe100K/",
    "/home/wilke/Data/UniKGE/caligraph_dbpedia_procrustes/"
]

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

# Ping webservice
statusCode = embeddings_cc_index.ping(seconds=1)
if statusCode == 502:
    print('502: Webservice unavailable')
    sys.exit(1)
elif statusCode == 503:
    print('503: Elasticsearch service unavailable')
    sys.exit(1)
else:
    print(statusCode)


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


# Wait some time if CPU usage is high
def optional_sleep(embeddings_cc_index, password):
    if int(embeddings_cc_index.get_max_cpu_usage(password).text) > 66:
        print('sleep', end=' ')
        sys.stdout.flush()
        time.sleep(60)
    if int(embeddings_cc_index.get_max_cpu_usage(password).text) > 33:
        print('sleep', end=' ')
        sys.stdout.flush()
        time.sleep(30)


# Parse files
for es_index, data_folder in zip(es_indices, data_folders):

    # Delete existing index
    print(f"\nUploading universal embeddings for {data_folder}\n")
    response = embeddings_cc_index.delete_index(password, es_index)
    if response.status_code == 200:
        print('Deleting index', response.status_code, response.text)

    # Read data
    print('\nLoading embeddings...\n')
    with open(data_folder + 'list_merged_entities.txt') as file:
        entities = file.read().split('\t')
    with open(data_folder + 'alignment.json') as file:
        alignment = json.load(file)
    embeddings = np.load(data_folder + 'Universal_Emb.npy', mmap_mode='r+')
    print('Done!\n')

    # Create index
    response = embeddings_cc_index.create_index(password, es_index, embeddings.shape[1], shards=5)
    print('Creating index', response.status_code, response.text)

    # Add data
    Embeddings = []
    print("\nDimensions:", embeddings.shape[1], "\n")
    assert len(entities) == embeddings.shape[0], f"{len(entities)}, {embeddings.shape[0]}"
    for i, ent in enumerate(entities):
        Embeddings.append([ent, list(embeddings[i])])

        if ent in alignment:
            Embeddings.append([alignment[ent], list(embeddings[i])])

        if i % 5000 == 0:
            if not add_embeddings(embeddings_cc_index, password, es_index, Embeddings):
                break
            Embeddings = []
            
            optional_sleep(embeddings_cc_index, password)

    optional_sleep(embeddings_cc_index, password)
    
    if len(Embeddings) > 0:
        add_embeddings(embeddings_cc_index, password, es_index, Embeddings)


# Print number of documents
# In tests, this resulted in 'httpcore.ReadTimeout: timed out'
if False:
    for es_index, data_folder in zip(es_indices, data_folders):
        response = embeddings_cc_index.count(es_index)
        print(response.status_code, response.text)

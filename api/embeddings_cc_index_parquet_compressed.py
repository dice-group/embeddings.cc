import sys
import ast
from embeddings_cc_index import EmbeddingsCcIndex
import polars
import json
import os

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

max_docs = 5000
if len(sys.argv) > 3:
    max_docs = sys.argv[3]
    
# Create instance
embeddings_cc_index = EmbeddingsCcIndex(webservice_url=webservice_url)

# Define the index and provide path to data
es_indices = ["dbpedia_wikidata_full"]#["dbp_en_fr_15k", "dbp_en_fr_100k", "dbp_en_de_100k"]
data_folders = ["Wiki-DBpedia/"] #["Shallom_EnFr_15K_V1/", "Shallom_EnFr_100K_V1/", "Experiments/EN_DE_100K_V1/"]

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
    
if True:

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
    for es_index, data_folder in zip(es_indices, data_folders):
        print("\n")
        print(f"Uploading universal embeddings for {data_folder}")
        print("\n")
        response = embeddings_cc_index.delete_index(password, es_index)
        print(response.status_code, response.text)
        file_path = base_path.split('embeddings.cc')[0]+data_folder
        print('\nLoading embeddings...\n')
        embeddings = polars.read_parquet(file_path+'/entity_embeddings_parquet', use_pyarrow=True).to_pandas()
        print('Done!\n')
        response = embeddings_cc_index.create_index(password, es_index, embeddings.shape[1]-1, shards=5)
        print(response.status_code, response.text)
        Embeddings = []
        print()
        for i,value in enumerate(embeddings.values):
            name, emb = value[-1], list(value[:-1])
            if '/entity/' in name:
                name = name.replace('embedding.cc', 'www.wikidata.org')
            else:
                name = name.replace('embedding.cc', 'dbpedia.org')
            Embeddings.append([name.strip("<>"), emb])
            if i % max_docs == 0:
                if not add_embeddings(embeddings_cc_index, password, es_index, Embeddings):
                    break
                Embeddings = []
        if len(Embeddings) > 0:
            add_embeddings(embeddings_cc_index, password, es_index, Embeddings)
        # Print number of documents
        response = embeddings_cc_index.count(es_index)
        print(response.status_code, response.text)

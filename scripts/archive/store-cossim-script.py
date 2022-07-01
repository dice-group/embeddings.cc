# embeddings.cc Cosine similarity script
# https://github.com/dice-group/embeddings.cc
#
# "Stored scripts reduce compilation time and make searches faster."
# https://www.elastic.co/guide/en/elasticsearch/reference/7.16/modules-scripting-using.html#script-stored-scripts
#
# Usage:
# - Set passwords and indexes below
# - python3 scripts/store-cossim-script.py

from elasticsearch import Elasticsearch

# Config
es_host     = 'http://localhost:9200'
es_user     = 'elastic'
es_password = ''

es_index   = 'index_test'
embeddings = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

do_store = False
do_query = False

# Store
# https://elasticsearch-py.readthedocs.io/en/v7.16.0/api.html#elasticsearch.Elasticsearch.put_script
if do_store:
    es = Elasticsearch(es_host, http_compress=True, http_auth=(es_user, es_password))

    result = es.put_script(id="cossim", body={
        "script": {
            "lang": "painless",
            "source": "cosineSimilarity(params['query_vector'], 'embeddings') + 1.0",
        }
    })

    print(result)

# Query
# https://www.elastic.co/guide/en/elasticsearch/reference/7.16/modules-scripting-using.html#script-stored-scripts
if do_query:
    es = Elasticsearch(es_host, http_compress=True, http_auth=(es_user, es_password))

    result = es.search(index=es_index, query={
        "script_score": {
            "query": {"match_all": {}},
            "script": {
                "id": "cossim",
                "params": {
                    "query_vector": embeddings
                }
            }
        }
    })

    print(result)

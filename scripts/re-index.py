  GNU nano 5.4                                                        /opt/embeddings_cc_b/scripts/re-index.py                                                                   
# embeddings.cc re-index
# https://github.com/dice-group/embeddings.cc
#
# Usage:
# - Set passwords and indexes below
# - time python3 scripts/re-index.py

from elasticsearch import Elasticsearch

# Config
es_host = 'http://localhost:9200'
es_user = 'elastic'
es_password     = ''
es_index_source = 'caligraph_dbpedia_procrustes'
es_index_target = 'caligraph_dbpedia_procrustes_40shards'

do_reindex = False

# Re-index
if do_reindex:
    es = Elasticsearch(es_host, http_compress=True, http_auth=(es_user, es_password))

    result = es.reindex(body={
        "source": {"index": es_index_source},
        "dest":   {"index": es_index_target}
    },
    wait_for_completion=True,
    request_timeout=10000)

    print(result)


from elasticsearch import Elasticsearch
from flask import current_app, g


def _make_es(host, user=None, password=None):
    es_kwargs = {
        'hosts': [host],
        'http_compress': True,
        'verify_certs': False,
        'timeout': 60,
        'max_retries': 5,
        'retry_on_timeout': True
    }
    if user and password:
        es_kwargs['http_auth'] = (user, password)
    return Elasticsearch(**es_kwargs)

def get_es():
    if 'es' not in g:
        g.es = _make_es(
            current_app.config['ES_HOST'],
            current_app.config.get('ES_USER'),
            current_app.config.get('ES_PASSWORD'),
        )
    return g.es

def get_es_demo():
    if 'es_demo' not in g:
        host = (current_app.config.get('ES_HOST_DEMO') or '').strip()
        if not host:
            g.es_demo = None
        else:
            g.es_demo = _make_es(
                host,
                current_app.config.get('ES_USER_DEMO'),
                current_app.config.get('ES_PASSWORD_DEMO'),
            )
    return g.es_demo

def close_es(e=None):
    for key in ('es', 'es_demo'):
        es_client = g.pop(key, None)
        if es_client is not None:
            try:
                es_client.close()
            except Exception:
                pass


def init_es():
    es = get_es()


def init_app(app):
    app.teardown_appcontext(close_es)


def get_random_entities(index, size=10):
    response = get_es().search(index=index, size=size, query={
        "function_score": {
            "query": {"match_all": {}},
            "random_score": {}
        }})
    entities = []
    for hit in response['hits']['hits']:
        entities.append(hit['_source']['entity'])
    return entities


def get_entities(index, size=100, offset=0):
    response = get_es().search(index=index, body={
        "from": offset, "size": size, "query": {"match_all": {}}
    })
    entities = []
    for hit in response['hits']['hits']:
        entities.append(hit['_source']['entity'])
    return entities

def get_entities_demo(index, size=100, offset=0):
    client = get_es_demo()
    if client is None:
        return []
    
    response = client.search(index=index, body={
        "from": offset, "size": size, "query": {"match_all": {}}
    })
    return [hit["_source"]["entity"] for hit in response["hits"]["hits"]]


def search_prefix(index, search_term):
    response = get_es().search(index=index, query={
        "prefix": {
            "entity": {
                "value": search_term
            }}
    })
    entities = []
    for hit in response['hits']['hits']:
        entities.append(hit['_source']['entity'])
    return entities


def search_completion(index, search_term):
    response = get_es().search(index=index, body={
        "suggest": {
            "suggestions": {
                "prefix": search_term,
                "completion": {
                    "field": "entity_completion"
                }
            }
        }
    })
    entities = []
    for hit in response['suggest']["suggestions"][0]["options"]:
        entities.append(hit['_source']['entity'])
    return entities


def get_dimensions(index):
    response = get_es().search(index=index, body={
        "from": 0, "size": 1, "query": {"match_all": {}}
    })
    return len(response['hits']['hits'][0]['_source']['embeddings'])

def get_embeddings(index, entities):
    return get_embeddings_from_client(get_es(), index, entities)

def get_embeddings_from_client(client, index, entities):
    if client is None:
        return []
    
    request = []
    for entity in entities:
        req_head = {'index': index}
        req_body = {'query': {"match": {
            'entity': entity
        }}}
        request.extend([req_head, req_body])
    response = client.msearch(body=request)
    results = []
    for resp in response['responses']:
        for hit in resp['hits']['hits']:
            results.append((hit['_source']['entity'], hit['_source']['embeddings']))
    return results

def get_embeddings_demo(index, entities):
    return get_embeddings_from_client(get_es_demo(), index, entities)


def get_similar_embeddings_cossim(index, embeddings):
    # similar embeddings based on cosine similarity
    request = []
    for embedding in embeddings:
        req_head = {'index': index}
        req_body = {"query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'embeddings') + 1.0",
                    "params": {
                        "query_vector": embedding
                    }
                }
            }
        }}
        request.extend([req_head, req_body])
    response = get_es().msearch(body=request)
    results = []
    for i, resp in enumerate(response['responses']):
        for hit in resp['hits']['hits']:
            results.append((i, hit['_score'] - 1, hit['_source']['entity'], hit['_source']['embeddings']))
    return results

def get_similar_embeddings(es, index, embeddings, k=10, num_candidates=100):
    msearch_body = []
    for vec in embeddings:
        msearch_body.append({"index": index})
        msearch_body.append({
            "size": k,
            "query": {
                "script_score": {
                    "query": { "match_all": {} },
                    "script": {
                        "source": "cosineSimilarity(params.qvec, 'embeddings') + 1.0",
                        "params": { "qvec": vec }
                    }
                }
            }
        })

    resp = es.msearch(body=msearch_body)

    results = []
    for i, sub in enumerate(resp["responses"]):
        for hit in sub["hits"]["hits"]:
            classic_score = hit["_score"] - 1.0
            results.append((
                i,
                classic_score,
                hit["_source"]["entity"],
                hit["_source"]["embeddings"],
            ))
    return results


def log(epoch_second, ip, path, parameters):
    get_es().index(index='usagelog', body={
        'date': epoch_second,
        'ip': ip,
        'path': path,
        'parameters': parameters
    })


def get_log_paths():
    response = get_es().search(index='usagelog', body={"aggs": {"paths": {"terms": {"field": "path"}}}})
    results = {}
    for result in response['aggregations']['paths']['buckets']:
        results[result['key']] = result['doc_count']
    results['total'] = response['hits']['total']['value']
    return sorted(results.items(), key=lambda x: x[1], reverse=True)


def get_indices():
    indices = list(get_es().indices.get_alias().keys())
    indices.remove('usagelog')
    return [x for x in indices if 'security' not in x]


def get_aliases():
    aliases = []
    for index in get_es().indices.get_alias().items():
        index_aliases = list(index[1]['aliases'].keys())
        if index_aliases:
            aliases += index_aliases
    return [x for x in aliases if 'security' not in x]

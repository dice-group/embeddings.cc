from elasticsearch import Elasticsearch
from flask import current_app, g


def get_es():
    if 'es' not in g:
        if 'ES_USER' in current_app.config and current_app.config['ES_USER'] and 'ES_PASSWORD' in current_app.config and \
                current_app.config['ES_PASSWORD']:
            g.es = Elasticsearch(current_app.config['ES_HOST'], http_compress=True,
                                 http_auth=(current_app.config['ES_USER'], current_app.config['ES_PASSWORD']))
        else:
            g.es = Elasticsearch(current_app.config['ES_HOST'], http_compress=True)
    return g.es


def close_es(e=None):
    es = g.pop('es', None)

    if es is not None:
        es.close()


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
    response = get_es().search(index=index, size=size, body={
        "from": offset, "size": size, "query": {"match_all": {}}
    })
    entities = []
    for hit in response['hits']['hits']:
        entities.append(hit['_source']['entity'])
    return entities


def get_embeddings(index, entities):
    request = []
    for entity in entities:
        req_head = {'index': index}
        req_body = {'query': {"match": {
            'entity': entity
        }}}
        request.extend([req_head, req_body])
    response = get_es().msearch(body=request)
    results = []
    for resp in response['responses']:
        for hit in resp['hits']['hits']:
            results.append((hit['_source']['entity'], hit['_source']['embeddings']))
    return results


def get_similar_embeddings(index, embeddings):
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


def log(epoch_second, ip, path, parameters):
    get_es().index(index='logger', body={
        'date': epoch_second,
        'ip': ip,
        'path': path,
        'parameters': parameters
    })


def get_log_paths():
    response = get_es().search(index='logger', body={"aggs": {"paths": {"terms": {"field": "path"}}}})
    results = {}
    for result in response['aggregations']['paths']['buckets']:
        results[result['key']] = result['doc_count']
    results['total'] = response['hits']['total']['value']
    return sorted(results.items(), key=lambda x: x[1], reverse=True)

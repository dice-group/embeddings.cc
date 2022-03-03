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


def get_entities(index, max=10):
    response = get_es().search(index=index, query={
        "function_score": {
            "query": {"match_all": {}},
            "random_score": {}
        }})
    entities = []
    for i, hit in enumerate(response['hits']['hits']):
        entities.append(hit['_source']['entity'])
        if i + 1 >= max:
            break
    return entities


def get_embeddings_multi(index, entities):
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


def get_embeddings(index, entity):
    response = get_es().search(index=index, query={"match": {
        'entity': entity
    }})
    embeddings = []
    for hit in response['hits']['hits']:
        embeddings.append(hit['_source']['embeddings'])
    return embeddings


def get_similar(index, embedding):
    response = get_es().search(index=index, body={
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'embeddings') + 1.0",
                    "params": {
                        "query_vector": embedding
                    }
                }
            }
        }
    })
    hits = response['hits']['hits']

    print(hits)

    results = []
    for hit in hits:
        results.append((hit['_score'] - 1, hit['_source']['entity'], hit['_source']['embeddings']))
    return results

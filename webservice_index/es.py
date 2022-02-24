from elasticsearch import Elasticsearch
from flask import current_app, g


def get_es():
    if 'es' not in g:
        if 'ES_USER' in current_app.config and current_app.config['ES_USER'] and 'ES_PASSWORD' in current_app.config and current_app.config['ES_PASSWORD']:
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

from elasticsearch import Elasticsearch
from flask import current_app, g


def get_es():
    if 'es' not in g:
        g.es = Elasticsearch(current_app.config['ES_HOST'])
    return g.es


def close_es(e=None):
    es = g.pop('es', None)

    if es is not None:
        es.close()


def init_es():
    es = get_es()


def init_app(app):
    app.teardown_appcontext(close_es)
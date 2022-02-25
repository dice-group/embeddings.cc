import os
import traceback
import json
from flask import Flask, request
from flask_cors import cross_origin
from elasticsearch import ElasticsearchException
from . import security
from . import es


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    es.init_app(app)

    @app.route('/ping', methods=['GET'])
    @cross_origin()
    def ping():
        if not es.get_es().ping():
            return 'Elasticsearch service unavailable', 503
        else:
            return 'Status: OK', 200

    @app.route('/count', methods=['GET'])
    @cross_origin()
    def count():
        if not request.args.get('password') or not security.check_password(request.args.get('password')):
            return 'Unauthorized', 401

        if 'index' not in request.args or not request.args.get('index'):
            return 'Missing parameter index', 422
        else:
            index = request.args.get('index')

        try:
            return es.get_es().cat.count(index)
        except ElasticsearchException as e:
            return traceback.format_exc(), 503

    @app.route('/get_indexes', methods=['POST'])
    @cross_origin()
    def get_indexes():
        if not request.args.get('password') or not security.check_password(request.args.get('password')):
            return 'Unauthorized', 401
        try:
            return es.get_es().indices.get_alias("*")
        except ElasticsearchException as e:
            return traceback.format_exc(), 503

    @app.route('/create_index', methods=['POST'])
    @cross_origin()
    def create_index():
        if not request.args.get('password') or not security.check_password(request.args.get('password')):
            return 'Unauthorized', 401

        if 'index' not in request.args or not request.args.get('index'):
            return 'Missing parameter index', 422
        else:
            index = request.args.get('index')

        if 'dimensions' not in request.args or not request.args.get('dimensions'):
            return 'Missing parameter dimensions', 422
        else:
            dimensions = request.args.get('dimensions')

        number_of_shards = request.args.get('number_of_shards', 5)

        index_config = {
            'settings': {
                'number_of_shards': number_of_shards,
                'number_of_replicas': 1
            },
            'mappings': {
                'properties': {
                    'id': {
                        'type': 'keyword'
                    },
                    'entity': {
                        'type': 'keyword'
                    },
                    'embeddings': {
                        'type': 'dense_vector',
                        'dims': dimensions
                    }
                }
            }
        }

        try:
            return es.get_es().indices.create(index, body=index_config)
        except ElasticsearchException as e:
            return traceback.format_exc(), 503

    @app.route('/delete_index', methods=['POST'])
    @cross_origin()
    def delete_index():
        if not request.args.get('password') or not security.check_password(request.args.get('password')):
            return 'Unauthorized', 401

        if 'index' not in request.args or not request.args.get('index'):
            return 'Missing parameter index', 422
        else:
            index = request.args.get('index')

        if "security" in index: 
            return 'Not allowed to delete security', 422

        try:
            return es.get_es().indices.delete(index)
        except ElasticsearchException as e:
            return traceback.format_exc(), 503

    @app.route('/add', methods=['POST'])
    @cross_origin()
    def add():
        if not request.args.get('password') or not security.check_password(request.json['password']):
            return 'Unauthorized', 401

        if not request.json:
            return 'Missing json data', 422

        if 'index' not in request.json:
            return 'Missing parameter index', 422
        else:
            index = request.json['index']

        if 'docs' not in request.json:
            return 'Missing parameter docs', 422
        else:
            docs = request.json['docs']

        if len(docs) > 50000:
            return 'Too many records', 413

        documents = []
        for doc in docs:
            documents.append({
                "index": {
                    "_index": index
                }
            })
            documents.append({
                'entity': doc[0],
                'embeddings': doc[1]
            })

        try:
            return es.get_es().bulk(index=index, body=documents)
        except ElasticsearchException as e:
            return traceback.format_exc(), 503

    @app.route('/get_embeddings', methods=['GET'])
    @cross_origin()
    def get_embeddings():

        if 'index' not in request.args or not request.args.get('index'):
            return 'Missing parameter index', 422
        else:
            index = request.args.get('index')

        if 'entity' not in request.args or not request.args.get('entity'):
            return 'Missing parameter entity', 422
        else:
            entity = request.args.get('entity')

        response = es.get_es().search(index=index, body={
            'query': {
                'match': {
                    'entity': entity
                }
            }
        })

        results = {}
        for hit in response['hits']['hits']:
            entity = hit['_source']['entity']
            embeddings = hit['_source']['embeddings']
            if entity not in results:
                results[entity] = []
            results[entity].append(embeddings)
        return json.JSONEncoder().encode(results)

    return app

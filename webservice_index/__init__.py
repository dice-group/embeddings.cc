import os
import traceback
import json
import numbers
import re
import ast
from flask import Flask, request, current_app
from flask_cors import cross_origin
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

    # ----------| GET requests without password |-----------------------------------------------------------------------

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
        if 'index' not in request.args or not request.args.get('index'):
            return 'Missing parameter index', 422
        else:
            index = request.args.get('index')

        try:
            return str(es.get_es().cat.count(index=index))
        except Exception as e:
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

    # ----------| POST requests with password |-------------------------------------------------------------------------

    @app.route('/get_max_cpu_usage', methods=['POST'])
    @cross_origin()
    def get_max_cpu_usage():
        if not request.args.get('password') or not security.check_password(request.args.get('password')):
            return 'Unauthorized', 401
        results = "{}"
        try:
            results = es.get_es().nodes.stats(node_id="*", metric="process")
        except Exception as e:
            return traceback.format_exc(), 503
        results_dict = ast.literal_eval(str(results))
        cpu_max = 0
        for node_id in results_dict['nodes']:
            cpu_percent = results_dict['nodes'][node_id]['process']['cpu']['percent']
            if cpu_percent > cpu_max:
                cpu_max = cpu_percent
        return str(cpu_max)

    @app.route('/get_indexes', methods=['POST'])
    @cross_origin()
    def get_indexes():
        if not request.args.get('password') or not security.check_password(request.args.get('password')):
            return 'Unauthorized', 401
        try:
            return str(es.get_es().indices.get_alias(index="*"))
        except Exception as e:
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

        number_of_shards = request.args.get('shards', 5)

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
                    "entity_completion": {
                        "type": "completion"
                    },
                    'embeddings': {
                        'type': 'dense_vector',
                        'dims': dimensions,
                        
                        # KNN additions
                        'index': 'true',
                        'similarity': 'l2_norm'
                    }
                }
            }
        }

        try:
            return str(es.get_es().indices.create(index=index, body=index_config))
        except Exception as e:
            return traceback.format_exc(), 503

    @app.route('/create_index_usagelog', methods=['POST'])
    @cross_origin()
    def create_index_usagelog():
        if not request.args.get('password') or not security.check_password(request.args.get('password')):
            return 'Unauthorized', 401

        index_config = {
            'settings': {
                'number_of_shards': 2,
                'number_of_replicas': 1
            },
            'mappings': {
                'properties': {
                    "date": {
                        "type": "date",
                        "format": "epoch_second"
                    },
                    "ip": {
                        "type": "keyword"
                    },
                    'path': {
                        'type': 'keyword'
                    },
                    'parameters': {
                        'type': 'flattened'
                    }
                }
            }
        }

        try:
            return str(es.get_es().indices.create(index='usagelog', body=index_config))
        except Exception as e:
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

        if current_app.config['ES_INDEX'] == index:
            return 'Not allowed to delete default index ' + current_app.config['ES_INDEX'], 422
        elif index == "logger":
            return 'Not allowed to delete index logger', 422
        elif "security" in index:
            return 'Not allowed to delete index security', 422

        try:
            return str(es.get_es().indices.delete(index=index))
        except Exception as e:
            return traceback.format_exc(), 503

    @app.route('/add', methods=['POST'])
    @cross_origin()
    def add():
        index_entity = 0
        index_embeddings = 1

        if not request.json:
            return 'Missing json data', 422

        if 'password' not in request.json:
            return 'Missing parameter password', 422
        elif not security.check_password(request.json['password']):
            return 'Unauthorized', 401

        if 'index' not in request.json:
            return 'Missing parameter index', 422
        else:
            index = request.json['index']

        if 'docs' not in request.json:
            return 'Missing parameter docs', 422
        else:
            docs = request.json['docs']

        if len(docs) > 0:
            if not isinstance(docs[0][index_embeddings][0], numbers.Number):
                return 'Embeddings of first record not numeric', 422

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
                'entity': doc[index_entity],
                'embeddings': doc[index_embeddings],
                'entity_completion': re.split('[^A-Za-z0-9]+',  doc[index_entity].rsplit('/', 1)[-1])
            })

        try:
            return str(es.get_es().bulk(index=index, body=documents))
        except Exception as e:
            return traceback.format_exc(), 503

    @app.route('/alias_put', methods=['POST'])
    @cross_origin()
    def alias_put():
        if 'password' not in request.values:
            return 'Missing parameter password', 422
        elif not security.check_password(request.values['password']):
            return 'Unauthorized', 401

        if 'index' not in request.values:
            return 'Missing parameter index', 422
        else:
            index = request.values['index']

        if 'alias' not in request.values:
            return 'Missing parameter alias', 422
        else:
            alias = request.values['alias']

        try:
            return str(es.get_es().indices.put_alias(index=index, name=alias))
        except Exception as e:
            return traceback.format_exc(), 503

    @app.route('/alias_delete', methods=['POST'])
    @cross_origin()
    def alias_delete():
        if 'password' not in request.values:
            return 'Missing parameter password', 422
        elif not security.check_password(request.values['password']):
            return 'Unauthorized', 401

        if 'index' not in request.values:
            return 'Missing parameter index', 422
        else:
            index = request.values['index']

        if 'alias' not in request.values:
            return 'Missing parameter alias', 422
        else:
            alias = request.values['alias']

        try:
            return str(es.get_es().indices.delete_alias(index=index, name=alias))
        except Exception as e:
            return traceback.format_exc(), 503

    return app

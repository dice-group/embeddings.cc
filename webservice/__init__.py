import os
import traceback
import ast
from flask import Flask, request, current_app, jsonify
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

    @app.route('/api/v1/ping', methods=['GET'])
    @cross_origin()
    def ping():
        if not es.get_es().ping():
            return 'Status: Database unavailable', 503
        else:
            return 'Status: OK', 200

    @app.route('/api/v1/get_entities', methods=['GET'])
    @cross_origin()
    def get_entities():
        return jsonify(es.get_entities(current_app.config['ES_INDEX'], max=10))

    @app.route('/api/v1/get_embedding', methods=['GET'])
    @cross_origin()
    def get_embedding():
        if 'entity' not in request.args or not request.args.get('entity'):
            return 'Missing parameter entity', 422
        else:
            entity = request.args.get('entity')
        return jsonify(es.get_embeddings(current_app.config['ES_INDEX'], entity))

    @app.route('/api/v1/get_similar', methods=['GET'])
    @cross_origin()
    def get_similar():
        if 'embedding' not in request.args or not request.args.get('embedding'):
            return 'Missing parameter embedding', 422
        else:
            embedding = ast.literal_eval(request.args.get('embedding'))
        return jsonify(es.get_similar(current_app.config['ES_INDEX'], embedding))

    return app

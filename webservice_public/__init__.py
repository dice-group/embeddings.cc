import os
import traceback
import ast
from flask import Flask, request, current_app, jsonify, render_template
from flask_cors import cross_origin
from elasticsearch import ElasticsearchException
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

    @app.route('/')
    def index():
        entities = ''
        entity = ''
        if 'get_entities' in request.args and request.args.get('get_entities'):
            entity = request.args.get('entity')
            entities_results = es.get_entities(current_app.config['ES_INDEX'], max=5)
            for entities_result in entities_results:
                entities += entities_result + '\n'
            if len(entities_results) > 0:
                entity = entities_results[0]

        if 'entity' in request.args and request.args.get('entity'):
            entity = request.args.get('entity')

        embeddings = ''
        embedding = ''
        if 'entity' in request.args and request.args.get('entity'):
            embeddings_results = es.get_embeddings(current_app.config['ES_INDEX'], entity)
            for embeddings_result in embeddings_results:
                embeddings += str(embeddings_result) + '\n'
            if len(embeddings_results) >= 1:
                embedding = embeddings_results[0]

        similar_embeddings = ''
        if 'embedding' in request.args and request.args.get('embedding'):
            embedding = ast.literal_eval(request.args.get('embedding'))
            similar_embeddings = ''
            for e in es.get_similar(current_app.config['ES_INDEX'], embedding):

                similar_embeddings += str("{:.4f}".format(round(e[0], 4))) + '  '
                similar_embeddings += e[1] + '  '
                similar_embeddings += str(e[2]) + '\n'

        return render_template('index.htm', entities=entities,
                               entity=entity, embeddings=embeddings,
                               embedding=embedding, similar_embeddings=similar_embeddings)

    return app

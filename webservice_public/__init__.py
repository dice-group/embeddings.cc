import os
import traceback
import ast
from flask import Flask, request, current_app, jsonify, render_template
from flask_cors import cross_origin
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

    @app.route('/api/v1/get_random_entities', methods=['POST'])
    @cross_origin()
    def get_random_entities():
        size = 10
        if 'size' in request.values:
            size = int(request.values['size'])
        if size < 1 or size > 1000:
            return 'Incorrect value for parameter: size', 422
        return jsonify(es.get_random_entities(current_app.config['ES_INDEX'], size=size))

    @app.route('/api/v1/get_embeddings', methods=['POST'])
    @cross_origin()
    def get_embeddings():
        if 'entities' not in request.json or not request.json['entities']:
            return 'Missing parameter: entities', 422
        else:
            entities = request.json['entities']
        if len(entities) > 1000:
            return 'Incorrect value for parameter: entities', 422
        return jsonify(es.get_embeddings(current_app.config['ES_INDEX'], entities=entities))

    @app.route('/api/v1/get_similar_embeddings', methods=['POST'])
    @cross_origin()
    def get_similar_embeddings():
        if 'embeddings' not in request.json or not request.json.get('embeddings'):
            return 'Missing parameter: embeddings', 422
        else:
            embeddings = request.json['embeddings']
        if len(embeddings) > 1000:
            return 'Incorrect value for parameter: embeddings', 422
        for i, embedding in enumerate(embeddings):
            if current_app.config['ES_DIMENSIONS'] != len(embedding):
                return 'Incorrect dimensions (' + str(len(embedding)) + ' instead of ' + \
                       str(current_app.config['ES_DIMENSIONS']) + ') for embeddings index: ' + str(i), 422
        return jsonify(es.get_similar_embeddings(current_app.config['ES_INDEX'], embeddings))

    @app.route('/api/v1/get_similar_entities', methods=['POST'])
    @cross_origin()
    def get_similar_entities():
        embeddings = []
        for tup in get_embeddings().json:
            embeddings.append(tup[1])
        results = []
        for trip in es.get_similar_embeddings(current_app.config['ES_INDEX'], embeddings):
            results.append((trip[0], trip[1]))
        return jsonify(results)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        entities = ''
        entity = ''
        embeddings = ''
        embedding = ''
        similar_embeddings = ''
        if request.method == 'POST':

            # First form: Set entities and entity
            if 'get_entities' in request.values:
                entities_results = es.get_random_entities(current_app.config['ES_INDEX'], size=5)
                for entities_result in entities_results:
                    entities += entities_result + '\n'
                if len(entities_results) > 0:
                    entity = entities_results[0]
                entities = entities.rstrip()

            # Second form: Set embeddings and embedding
            if 'entity' in request.values and request.values['entity']:
                entity = request.values['entity']
                embeddings_results = es.get_embeddings(current_app.config['ES_INDEX'], [entity])
                for embeddings_result in embeddings_results:
                    embeddings += str(embeddings_result[1]) + '\n'
                if len(embeddings_results) >= 1:
                    embedding = embeddings_results[0][1]
                embeddings = embeddings.rstrip()

            # Third form: Set similar embeddings
            if 'embedding' in request.values and request.values['embedding'].startswith('['):
                embedding = ast.literal_eval(request.values['embedding'])
                if len(embedding) == current_app.config['ES_DIMENSIONS']:
                    results = es.get_similar_embeddings(current_app.config['ES_INDEX'], [embedding])
                    length = 0
                    for result in results:
                        if len(result[1]) > length:
                            length = len(result[1])
                    similar_embeddings = ''
                    for result in results:
                        similar_embeddings += result[1].ljust(length) + '  '
                        similar_embeddings += str("{:.4f}".format(round(result[0], 4))) + '  '
                        similar_embeddings += str(result[2]) + '\n'
                    similar_embeddings = similar_embeddings.rstrip()

        return render_template('index.htm',
                               entities=entities, entity=entity,
                               embeddings=embeddings, embedding=embedding,
                               similar_embeddings=similar_embeddings)

    return app

import os
import time
from flask import Flask, request, current_app, jsonify, render_template, send_from_directory
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

    # Webservices ------------------------------------------------------------------------------------------------------

    @app.route('/api/v1/ping', methods=['GET', 'POST'])
    @cross_origin()
    def ping():
        log()
        if not es.get_es().ping():
            return 'Status: Database unavailable', 503
        else:
            return 'Status: OK', 200

    @app.route('/api/v1/get_size', methods=['POST'])
    @cross_origin()
    def get_size():
        log()
        count_string = es.get_es().cat.count(index=get_index())
        return count_string[count_string.rindex(' ') + 1:]

    @app.route('/api/v1/get_random_entities', methods=['POST'])
    @cross_origin()
    def get_random_entities():
        size = 10
        if 'size' in request.json and request.json['size']:
            try:
                size = int(request.json['size'])
            except ValueError:
                return 'Incorrect type for parameter: size', 415
        if size < 1 or size > 100:
            return 'Incorrect value for parameter: size', 422
        log()
        return jsonify(es.get_random_entities(get_index(), size=size))

    @app.route('/api/v1/get_entities', methods=['POST'])
    @cross_origin()
    def get_entities():
        size = 100
        offset = 0
        if 'size' in request.json and request.json['size']:
            try:
                size = int(request.json['size'])
            except ValueError:
                return 'Incorrect type for parameter: size', 415
        if size < 1 or size > 10000:
            return 'Incorrect value for parameter: size', 422
        if 'offset' in request.json and request.json['offset']:
            try:
                offset = int(request.json['offset'])
            except ValueError:
                return 'Incorrect type for parameter: offset', 415
        if offset < 0:
            return 'Incorrect value for parameter: offset', 422
        log()
        return jsonify(es.get_entities(get_index(), size=size, offset=offset))

    @app.route('/api/v1/get_embeddings', methods=['POST'])
    @cross_origin()
    def get_embeddings():
        if 'entities' not in request.json or not request.json['entities']:
            return 'Missing parameter: entities', 422
        else:
            entities = request.json['entities']
        if len(entities) > 100:
            return 'Incorrect value for parameter: entities', 422
        log()
        return jsonify(es.get_embeddings(get_index(), entities=entities))

    @app.route('/api/v1/get_similar_embeddings', methods=['POST'])
    @cross_origin()
    def get_similar_embeddings():
        if 'embeddings' not in request.json or not request.json.get('embeddings'):
            return 'Missing parameter: embeddings', 422
        else:
            embeddings = request.json['embeddings']
        if len(embeddings) > 100:
            return 'Incorrect value for parameter: embeddings', 422
        for i, embedding in enumerate(embeddings):
            if es.get_dimensions(get_index()) != len(embedding):
                return 'Incorrect dimensions (' + str(len(embedding)) + ' instead of ' + \
                       str(es.get_dimensions(get_index())) + ') for embeddings index: ' + str(i), 422
        log()
        return jsonify(es.get_similar_embeddings(get_index(), embeddings))

    @app.route('/api/v1/get_similar_entities', methods=['POST'])
    @cross_origin()
    def get_similar_entities():
        if 'entities' not in request.json or not request.json['entities']:
            return 'Missing parameter: entities', 422
        else:
            entities = request.json['entities']
        if len(entities) > 100:
            return 'Incorrect value for parameter: entities', 422

        embeddings = []
        for tup in es.get_embeddings(get_index(), entities=entities):
            embeddings.append(tup[1])

        results = []
        for trip in es.get_similar_embeddings(get_index(), embeddings):
            results.append((trip[0], trip[1], trip[2]))
        log()
        return jsonify(results)

    # Website ----------------------------------------------------------------------------------------------------------

    @app.route('/', methods=['GET', 'POST'])
    def index():

        # Add links to indices for developers
        dev = ''
        index = ''
        if 'dev' in request.values:
            dev = es.get_indices()
        if 'index' in request.values:
            index = request.values['index']

        entities = []
        entity = ''
        embeddings = ''
        similar_entities = []
        if request.method == 'POST':
            matches = ["&amp;", "'"]

            # First form: Set entities and entity
            if 'get_entities' in request.values:
                entities_results = es.get_random_entities(get_index(), size=15)
                for entities_result in entities_results:
                    if any(x in entities_result for x in matches):
                        continue

                    title = entities_result
                    if 'fr.dbpedia.org/resource/' in title:
                        title = title[24 + title.index('fr.dbpedia.org/resource/'):].replace('_', ' ') + ' (fr)'
                    elif 'dbpedia.org/resource/' in title:
                        title = title[21 + title.index('dbpedia.org/resource/'):].replace('_', ' ')
                    elif 'http://caligraph.org/ontology/' in title:
                        title = title[30 + title.index('http://caligraph.org/ontology/'):].replace('_', ' ')
                    entities.append((entities_result, title))

                entity = entities[0][0]

            # Third form: Set embeddings and embedding
            if 'entity' in request.values and request.values['entity']:
                entity = request.values['entity']
                embeddings_results = es.get_embeddings(get_index(), [entity])
                if len(embeddings_results) > 0:
                    embeddings = embeddings_results[0][1]

            # Second form: Set similar embeddings
            if 'similarity' in request.values and request.values['similarity']:
                entity = request.values['similarity']
                embeddings_results = es.get_embeddings(get_index(), entities=[entity])
                if len(embeddings_results) > 0:
                    similar_entities = []
                    for tup in es.get_similar_embeddings(get_index(),
                                                         embeddings=[embeddings_results[0][1]]):
                        if any(x in tup[2] for x in matches):
                            continue

                        title = tup[2]
                        if 'fr.dbpedia.org/resource/' in title:
                            title = title[24 + title.index('fr.dbpedia.org/resource/'):].replace('_', ' ') + ' (fr)'
                        elif 'dbpedia.org/resource/' in title:
                            title = title[21 + title.index('dbpedia.org/resource/'):].replace('_', ' ')
                        elif 'http://caligraph.org/ontology/' in title:
                            title = title[30 + title.index('http://caligraph.org/ontology/'):].replace('_', ' ')
                        similar_entities.append((str("{:.4f}".format(round(tup[1], 4))),
                                                 tup[2],
                                                 title))

        log()
        return render_template('index.htm', entities=entities, entity=entity,
                               embeddings=embeddings, similar_entities=similar_entities,
                               dev=dev, index=index)

    @app.route('/api', methods=['GET'])
    def api():
        log()
        return render_template('api.htm')

    @app.route('/news', methods=['GET'])
    def news():
        log()
        return render_template('news.htm')

    @app.route('/usage', methods=['GET'])
    def usage():
        log()
        return jsonify(es.get_log_paths())

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'),
                                   'favicon.ico', mimetype='image/vnd.microsoft.icon')

    # Helpers ----------------------------------------------------------------------------------------------------------

    def get_index():
        if request.json and 'index' in request.json and request.json['index']:
            return request.json['index']
        elif request.values and 'index' in request.values and request.values['index']:
            return request.values['index']
        else:
            return current_app.config['ES_INDEX']

    def log():
        es.log(int(time.time()), request.remote_addr, request.path, request.args)

    return app

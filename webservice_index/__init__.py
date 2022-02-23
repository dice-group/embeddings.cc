import os
from flask import Flask, request
from flask_cors import cross_origin


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

    from . import security

    from . import es
    es.init_app(app)

    @app.route('/ping', methods=['GET'])
    @cross_origin()
    def ping():
        return 'Status: OK', 200

    @app.route('/get_indexes', methods=['POST'])
    @cross_origin()
    def get_indexes():
        if not security.check_password(request.args.get('password')):
            return 'Unauthorized', 401

        return es.get_es().indices.get_alias("*")

    @app.route('/create_index', methods=['POST'])
    @cross_origin()
    def create_index():
        if not security.check_password(request.args.get('password')):
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
                'number_of_shards': number_of_shards,                              # TODO is 5 the best parameter?
                'number_of_replicas': 1
            },
            'mappings': {
                'properties': {
                    'id': {
                        'type': 'keyword'
                    },
                    'entity': {
                        'type': 'keyword'                              # TODO Why same id and entity?
                    },
                    'embeddings': {
                        'type': 'dense_vector',
                        'dims': dimensions
                    }
                }
            }
        }
        return es.get_es().indices.create(index, body=index_config)

    @app.route('/delete_index', methods=['POST'])
    @cross_origin()
    def delete_index():
        if not security.check_password(request.args.get('password')):
            return 'Unauthorized', 401

        if 'index' not in request.args or not request.args.get('index'):
            return 'Missing parameter index', 422
        else:
            index = request.args.get('index')

        return es.get_es().indices.delete(index)

    # @app.route('/add_docs', methods=['GET'])                               # TODO POST
    # @cross_origin()
    # def add_docs():
    #     if not security.check_password(request.args.get('password')):
    #         return 'Unauthorized', 401
    #
    #     if 'index' not in request.args or not request.args.get('index'):
    #         return 'Missing parameter index', 422
    #     else:
    #         index = request.args.get('index')
    #
    #     if 'docs' not in request.args or not request.args.get('docs'):
    #         return 'Missing parameter docs', 422
    #     else:
    #         docs = request.json['docs']
    #
    #     for doc in docs:
    #         print(doc)
    #
    #     return 'cool'








    return app

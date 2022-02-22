import os
import hashlib
from flask import Flask, current_app, request
from flask_cors import cross_origin
from elasticsearch import Elasticsearch


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

    @app.route('/ping', methods=['GET'])
    @cross_origin()
    def ping():
        return "Status: OK", 200

    @app.route('/get_indexes', methods=['GET'])  # TODO POST
    @cross_origin()
    def get_indexes():
        if current_app.config['PSW_SALT_HASH'] != hashlib.pbkdf2_hmac(
                'sha256',
                request.args.get('password', '').encode('utf-8'),
                current_app.config['SALT'],
                100000):
            return "Unauthorized", 401
        return Elasticsearch(current_app.config['ES_HOST']).indices.get_alias("*")

    return app

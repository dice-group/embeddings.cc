import os
import json
import random
import time
import hashlib
import ipaddress
import httpx
from urllib.parse import urlsplit
from flask import Flask, request, current_app, jsonify, render_template, send_from_directory
from flask_cors import cross_origin
from . import es


DEMO_SPARQL_GRAPHS = {
    'wikidata': 'https://data.embeddings.cc/wikidata',
    'dbpedia': 'https://data.embeddings.cc/dbpedia',
}


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

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('500.html'), 500

    @app.route('/autocomplete', methods=['GET'])
    @cross_origin()
    def dev():
        if request.args.get('search_term'):
            return jsonify(es.search_completion(get_index(), request.args.get('search_term')))
        else:
            return jsonify([])

    @app.route('/api/v1/ping', methods=['GET', 'POST'])
    @cross_origin()
    def ping():
        log()
        if not es.get_es().ping():
            return 'Status: Database unavailable', 503
        else:
            return 'Status: OK', 200

    @app.route('/api/v1/get_indices', methods=['POST'])
    @cross_origin()
    def get_indices():
        log()
        return jsonify(es.get_aliases())

    @app.route('/api/v1/get_size', methods=['POST'])
    @cross_origin()
    def get_size():
        log()

        payload = request.get_json(silent=True) or {}

        index = payload.get('index') or get_index()

        count_string = es.get_es().cat.count(index=index)

        count = count_string.strip().split()[-1]

        return jsonify(count=int(count))

    @app.route('/api/v1/get_random_entities', methods=['POST'])
    @cross_origin()
    def get_random_entities():
        log()

        payload = request.get_json(silent=True) or {}

        index = payload.get('index') or get_index()

        size = 10
        if 'size' in request.json and request.json['size']:
            try:
                size = int(request.json['size'])
            except ValueError:
                return 'Incorrect type for parameter: size', 415
        if size < 1 or size > 100:
            return 'Incorrect value for parameter: size', 422

        entities = es.get_random_entities(index, size=size)
        return jsonify(entities)

    @app.route('/api/v1/get_entities', methods=['POST'])
    @cross_origin()
    def get_entities():
        log()

        payload = request.get_json(silent=True) or {}

        index = payload.get('index') or get_index()

        size = payload.get('size', 100)
        try:
            size = int(size)
        except (TypeError, ValueError):
            return 'Incorrect type for parameter: size', 415
        if size < 1 or size > 10000:
            return 'Incorrect value for parameter: size', 422

        offset = payload.get('offset', 0)
        try:
            offset = int(offset)
        except (TypeError, ValueError):
            return 'Incorrect type for parameter: offset', 415
        if offset < 0:
            return 'Incorrect value for parameter: offset', 422

        entities = es.get_entities(index, size=size, offset=offset)
        return jsonify(entities)

    @app.route('/api/v1/get_embeddings', methods=['POST'])
    @cross_origin()
    def get_embeddings():
        log()

        data = request.get_json(silent=True)
        if data is None:
            return 'Invalid or missing JSON body', 415

        if isinstance(data, list):
            entities = data
            index = get_index()

        elif isinstance(data, dict):
            entities = data.get('entities')
            index = data.get('index') or get_index()
        else:
            return 'JSON body must be an object or array', 415

        if not entities:
            return 'Missing parameter: entities', 422
        if not isinstance(entities, list):
            return 'Incorrect type for parameter: entities', 415
        if len(entities) > 100:
            return 'Incorrect value for parameter: entities', 422

        return jsonify(es.get_embeddings(index, entities=entities))

    @app.route('/api/v1/get_similar_embeddings', methods=['POST'])
    @cross_origin()
    def api_get_similar_embeddings():
        payload = request.get_json(force=True)

        embeddings = payload.get('embeddings')
        if not embeddings:
            return "Missing parameter: embeddings", 422
        if len(embeddings) > 100:
            return "Incorrect value for parameter: embeddings", 422

        client = es.get_es()
        idx = get_index()
        dims = es.get_dimensions(idx)
        for i, emb in enumerate(embeddings):
            if len(emb) != dims:
                return (f"Incorrect dimensions ({len(emb)} instead of {dims}) for index {i}", 422)

        try:
            results = es.get_similar_embeddings(client, idx, embeddings)
        except Exception as e:
            return f"Error querying Elasticsearch: {e}", 500

        return jsonify(results)

    @app.route('/api/v1/get_similar_entities', methods=['POST'])
    @cross_origin()
    def api_get_similar_entities():
        payload = request.get_json(force=True)

        entities = payload.get('entities')

        if not entities:
            return 'Missing parameter: entities', 422
        if len(entities) > 100:
            return 'Incorrect value for parameter: entities', 422

        client = es.get_es()
        idx = get_index()
        dims = es.get_dimensions(idx)
        embeddings = []
        for i, tup in enumerate(es.get_embeddings(idx, entities=entities)):
            vec = tup[1]
            if len(vec) != dims:
                return (
                    f"Incorrect dimensions ({len(vec)} instead of {dims}) for entity at position {i}",
                    422
                )
            embeddings.append(vec)

        try:
            sims = es.get_similar_embeddings(client, idx, embeddings)
        except Exception as e:
            return f"Error querying Elasticsearch: {e}", 500

        results = [(qi, score, entity) for qi, score, entity, _ in sims]
        log()
        return jsonify(results)

    # Website ----------------------------------------------------------------------------------------------------------

    @app.route('/', methods=['GET'])
    def index():

        log()
        return render_template('index.htm')

    @app.route('/old', methods=['GET', 'POST'])
    def old():

        # Add links to indices for developers
        dev = ''
        index = ''
        if 'dev' in request.values:
            dev = es.get_indices()
        if 'index' in request.values:
            index = request.values['index']

        index_size = es.get_es().cat.count(index=get_index())
        index_size = index_size[index_size.rindex(' ') + 1:]
        index_size = f'{int(index_size):,}'

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
        return render_template('universal-knowledge-graph.htm', entities=entities, entity=entity,
                               embeddings=embeddings, similar_entities=similar_entities,
                               dev=dev, index=index, index_size=index_size)

    def get_api_entries():
        entries = []
        for endpoint, view_fn in app.view_functions.items():
            if endpoint == 'static':
                continue

            for rule in app.url_map.iter_rules(endpoint):
                if not rule.rule.startswith('/api/v1/'):
                    continue

                path = rule.rule
                slug = path.rsplit('/', 1)[-1]
                methods = [m for m in rule.methods
                            if m in ('GET', 'POST', 'PUT', 'DELETE', 'PATCH')]

                entries.append({
                    'path': path,
                    'slug': slug,
                    'description': getattr(view_fn, 'api_description', ''),
                    'example': getattr(view_fn, 'api_example', ''),
                    'methods': methods,
                })
        
        return entries

    @app.route('/api', methods=['GET'])
    def api():
        log()
        return render_template(
            'api.htm',
            page_title='API',
            api_entries = get_api_entries()
            )

    @app.route('/news', methods=['GET'])
    def news():
        log()
        return render_template('news.htm', page_title='News')

    @app.route('/whale/embeddings', methods=['POST'])
    def whale_embeddings():
        data = request.get_json(force=True)
        entity = data.get('entity', '').strip()

        if not entity:
            return jsonify(embeddings=[]), 200

        try:
            results = es.get_embeddings('whale', [entity])
            embeddings = results[0][1] if results else ''
        except Exception as e:
            app.logger.warning(f"ES get_embeddings failed: {e}")
            embeddings = []
        return jsonify(embeddings=embeddings)
    
    @app.route('/demo/embeddings', methods=['POST'])
    def demo_embeddings():
        data = request.get_json(silent=True) or {}
        entity = (data.get('entity') or '').strip()
        index = (data.get('index') or '').strip()

        if not entity or not index:
            return jsonify(embeddings=[]), 200
        
        try:
            results = es.get_embeddings_demo(index, [entity])
            embeddings = results[0][1] if results else []
        except Exception as e:
            app.logger.warning(f"Demo ES get_embeddings failed ({index}): {e}")
            embeddings = []

        return jsonify(embeddings=embeddings), 200
    
    @app.route('/demo/entities', methods=['POST'])
    def demo_entities():
        data = request.get_json(silent=True) or {}
        index = (data.get('index') or '').strip()
        if not index:
            return jsonify(entities=[]), 200
        
        size = int(data.get('size', 100) or 100)
        offset = int(data.get('offset', 0) or 0)

        try:
            entities = es.get_entities_demo(index, size=size, offset=offset)
        except Exception as e:
            app.logger.warning(f"Demo ES get_entities failed ({index}): {e}")
            entities = []

        return jsonify(entities=entities), 200

    @app.route('/whale/entities', methods=['GET'])
    def whale_entities():
        try:
            entities = es.get_random_entities('whale', size=5)
        except Exception as e:
            app.logger.warning(f"ES get_random_entites failed: {e}")
            entities = []
        return jsonify(entities=entities)

    @app.route('/whale/random_uris', methods=['GET'])
    def random_uris():
        path = os.path.join(current_app.instance_path, 'uris.json')
        try:
            with open(path, 'r') as f:
                entities = json.load(f)
        except Exception:
            return jsonify(entities=[]), 200

        picks = random.sample(entities, min(15, len(entities)))

        return jsonify(entities=picks), 200
    
    @app.route('/demo/random_uris_global', methods=['GET'])
    def demo_random_uris_global():
        path = os.path.join(current_app.instance_path, 'uris_demo_global.json')
        try:
            with open(path, 'r', encoding='utf-8') as f:
                entities = json.load(f)
        except Exception:
            return jsonify(entities=[]), 200
        
        picks = random.sample(entities, min(15, len(entities)))
        return jsonify(entities=picks), 200

    @app.route('/demo/random_uris_sparql', methods=['GET'])
    def demo_random_uris_sparql():
        source = (request.args.get('source') or '').strip().lower()
        graph = DEMO_SPARQL_GRAPHS.get(source)
        if graph is None:
            return jsonify(error='Unsupported entity source'), 400

        query = f'''SELECT DISTINCT ?entity
WHERE {{
  GRAPH <{graph}> {{
    ?entity ?p ?o .
  }}
}}
LIMIT 100'''

        endpoint = current_app.config.get(
            'SPARQL_ENDPOINT',
            'https://sparql.embeddings.cc/sparql'
        )

        try:
            response = httpx.post(
                endpoint,
                data={'query': query},
                headers={'Accept': 'application/sparql-results+json'},
                timeout=30.0,
            )
            response.raise_for_status()
            bindings = response.json().get('results', {}).get('bindings', [])
            entities = [
                binding['entity']['value']
                for binding in bindings
                if binding.get('entity', {}).get('type') == 'uri'
                and binding['entity'].get('value')
            ]
        except (httpx.HTTPError, ValueError, TypeError, KeyError) as e:
            app.logger.warning(f"SPARQL random entities failed ({source}): {e}")
            return jsonify(error='SPARQL endpoint unavailable'), 502

        picks = random.sample(entities, min(15, len(entities)))
        return jsonify(entities=picks), 200

    @app.route('/demo/embeddings_sparql', methods=['POST'])
    def demo_embeddings_sparql():
        data = request.get_json(silent=True) or {}
        source = (data.get('source') or '').strip().lower()
        entity = (data.get('entity') or '').strip()
        graph = DEMO_SPARQL_GRAPHS.get(source)

        if graph is None:
            return jsonify(error='Unsupported entity source'), 400

        parsed_entity = urlsplit(entity)
        invalid_iri_characters = '<>"{}|^`\\\n\r\t '
        if (
            parsed_entity.scheme not in ('http', 'https')
            or not parsed_entity.netloc
            or any(character in entity for character in invalid_iri_characters)
        ):
            return jsonify(error='Invalid entity IRI'), 400

        query = f'''SELECT ?embedding
WHERE {{
  GRAPH <{graph}> {{
    <{entity}>
      <https://ontology.embeddings.cc/hasKeciEmbeddings>
      ?embedding .
  }}
}}'''

        endpoint = current_app.config.get(
            'SPARQL_ENDPOINT',
            'https://sparql.embeddings.cc/sparql'
        )

        try:
            response = httpx.post(
                endpoint,
                data={'query': query},
                headers={'Accept': 'application/sparql-results+json'},
                timeout=30.0,
            )
            response.raise_for_status()
            bindings = response.json().get('results', {}).get('bindings', [])

            if not bindings:
                return jsonify(embeddings=[]), 200

            embedding_value = bindings[0].get('embedding', {}).get('value')
            embeddings = json.loads(embedding_value)
            if (
                not isinstance(embeddings, list)
                or not all(
                    isinstance(value, (int, float)) and not isinstance(value, bool)
                    for value in embeddings
                )
            ):
                raise ValueError('Invalid embedding vector')
        except (httpx.HTTPError, ValueError, TypeError, KeyError) as e:
            app.logger.warning(f"SPARQL embeddings failed ({source}): {e}")
            return jsonify(error='SPARQL endpoint unavailable'), 502

        return jsonify(embeddings=embeddings), 200

    @app.route('/whale/count', methods=['GET'])
    def whale_count():
        client = es.get_es()
        try:
            whale_response = client.count(index='whale', request_timeout=30)
            whale_count = int(whale_response.get('count', 0))

            sparql_endpoint = current_app.config.get(
                'SPARQL_ENDPOINT',
                'https://sparql.embeddings.cc/sparql'
            )

            sparql_counts = {}
            with httpx.Client(timeout=30.0) as sparql_client:
                for source, graph in DEMO_SPARQL_GRAPHS.items():
                    sparql_query = f'''SELECT (COUNT(*) AS ?tripleCount)
WHERE {{
  GRAPH <{graph}> {{
    ?s ?p ?o .
  }}
}}'''
                    sparql_response = sparql_client.post(
                        sparql_endpoint,
                        data={'query': sparql_query},
                        headers={'Accept': 'application/sparql-results+json'},
                    )
                    sparql_response.raise_for_status()
                    bindings = sparql_response.json().get(
                        'results', {}
                    ).get('bindings', [])
                    sparql_counts[source] = int(
                        bindings[0]['tripleCount']['value']
                    )

            source_counts = {'wdc': whale_count, **sparql_counts}
            return {
                'count': sum(source_counts.values()),
                'sources': source_counts,
            }
        except Exception as e:
            app.logger.warning(f"Combined embeddings count failed: {e}")
            return {'count': None}, 503

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
        json_data = request.get_json(silent=True)
        if json_data and 'index' in json_data and json_data['index']:
            return json_data['index']
        elif request.values and 'index' in request.values and request.values['index']:
            return request.values['index']
        else:
            return current_app.config['ES_INDEX']

    def get_ip_hashes():
        ipv4 = request.remote_addr
        ipv6 = ipaddress.IPv6Address('2002::' + ipv4).exploded
        hashes = []
        for part in ipv6.split(':'):
            hashes.append(hashlib.shake_256(part.encode()).hexdigest(1))
        return hashes[:-1]

    def log():
        es.log(int(time.time()), get_ip_hashes(), request.path, request.args)

    return app

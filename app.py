from flask import Flask, request
from flask_cors import CORS, cross_origin
from elasticsearch import Elasticsearch
from jproperties import Properties

configs = Properties()
with open('app.props', 'rb') as config_file:
    configs.load(config_file)
app = Flask(__name__)
cors = CORS(app)
es = Elasticsearch(["http://nel.cs.upb.de:9200"],
                   http_auth=(configs.get("elastic.user").data, configs.get("elastic.password").data))


@app.route('/ping', methods=['GET'])
@cross_origin()
def test():
    return "Status:\tOK", 200


def get_embeddings(query_string, index_name, field_name='entity', first_n=1):
    res = es.search(index=index_name, body={
        "query": {
            "match": {
                field_name: query_string
            }
        }
    })
    hits = res['hits']['hits']
    if len(hits) > 0:
        results = []
        for i in range(max(first_n, len(hits))):
            results.append(hits[i]['_source'])
        return results
    return None


@app.route('/get-entity-embedding', methods=['GET'])
@cross_origin()
def get_entity_embedding():
    if "entities" not in request.json:
        return "Invalid parameters", 400
    entities = request.json["entities"]
    embeddings = {}
    for entity in entities:
        if entity in embeddings:
            continue
        embeddings[entity] = get_embeddings(entity, "embedding_index")[0]['embeddings']
        if len(embeddings.keys()) >= 10:
            break
    return embeddings


@app.route('/get-entity-index-info', methods=['GET'])
@cross_origin()
def get_entity_index_info():
    settings = es.indices.get(index="embedding_index")
    return settings["embedding_index"]["mappings"]


@app.route('/get-relation-index-info', methods=['GET'])
@cross_origin()
def get_relation_index_info():
    settings = es.indices.get(index="relation_embedding_index")
    return settings["relation_embedding_index"]["mappings"]


@app.route('/get-relation-embedding', methods=['GET'])
@cross_origin()
def get_relation_embedding():
    if "relations" not in request.json:
        return "Invalid parameters", 400
    entities = request.json["relations"]
    embeddings = {}
    for entity in entities:
        if entity in embeddings:
            continue
        hits = get_embeddings(entity, "relation_embedding_index", "relation", 4)
        embeddings[entity] = {
            'real': {
                'rhs': [],
                'lhs': []
            },
            'imag': {
                'rhs': [],
                'lhs': []
            }
        }
        for hit in hits:
            embeddings[entity][hit['dtype']][hit['operator']] = hit['embeddings']
        if len(embeddings.keys()) >= 10:
            break
    return embeddings


if __name__ == '__main__':
    app.run(debug=True)
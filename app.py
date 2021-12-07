from flask import Flask, request
from flask_cors import CORS, cross_origin
from elasticsearch import Elasticsearch

app = Flask(__name__)
cors = CORS(app)
es = Elasticsearch(["http://localhost:9200"])


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
    index_name = request.json["indexname"]
    embeddings = {}
    for entity in entities:
        if entity in embeddings:
            continue
        embeddings[entity] = get_embeddings(entity, index_name)[0]['embeddings']
        if len(embeddings.keys()) >= 10:
            break
    return embeddings


@app.route('/get-index-info', methods=['GET'])
@cross_origin()
def get_index_info():
    index_name = request.json["indexname"]
    settings = es.indices.get(index=index_name)
    return settings["embedding_index"]["mappings"]


if __name__ == '__main__':
    app.run(debug=True)

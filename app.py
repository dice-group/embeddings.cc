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


def get_embeddings_neighbour(query_embedding, index_name, field_name='embeddings', first_n=1):
    res = es.search(index=index_name, body={
        "query": {
            "script_score": {
                "query": {
                    "bool": {
                    }
                },
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'embeddings' ) + 1.0",
                    "params": {
                        "query_vector": query_embedding
                    }
                }
            }
        }
    })
    hits = res['hits']['hits']
    if len(hits) > 0:
        results = []
        for i in range(max(first_n, len(hits))):
            results.append(hits[i]['_source'])
        print(results)
        return results
    return None

@app.route('/get-index-list', methods=['GET'])
@cross_origin()
def get_index_list():
    indexes = {}
    indexes["index_list"] = list(es.indices.get_alias().keys());
    return indexes


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


@app.route('/get-entity-embedding-neighbour', methods=['GET'])
@cross_origin()
def get_entity_embedding_neighbour():
    if "embedding" not in request.json:
        return "Invalid parameters", 400
    embedding = request.json["embedding"]
    index_name = request.json["indexname"]
    neighbours = get_embeddings_neighbour(embedding, index_name)
    result = {
        "neighbours" : neighbours
    }
    return result

@app.route('/get-entity-neighbour', methods=['GET'])
@cross_origin()
def get_entity_neighbour():
    if "entity" not in request.json:
        return "Invalid parameters", 400
    entity = request.json["entity"]
    index_name = request.json["indexname"]
    embedding = get_embeddings(entity, index_name)[0]['embeddings']
    neighbours = get_embeddings_neighbour(embedding, index_name)
    result = {
        "neighbours": neighbours
    }
    return result



@app.route('/get-index-info', methods=['GET'])
@cross_origin()
def get_index_info():
    if "indexname" not in request.json:
        return "Invalid parameters", 400
    index_name = request.json["indexname"]
    settings = es.indices.get(index=index_name)
    return settings


if __name__ == '__main__':
    app.run(debug=True)


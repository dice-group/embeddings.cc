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


@app.route('/get-index-info', methods=['GET'])
@cross_origin()
def get_index_info():
    index_name = request.json["indexname"]
    settings = es.indices.get(index=index_name)
    return settings[index_name]["mappings"]


if __name__ == '__main__':
    app.run(debug=True)

[{'id': 99999, 'entity': '/resource/2010_European_Pairs_Speedway_Championship',
  'embeddings': [0.02009118, 0.0026167436, 0.04765874, -0.004239331, 0.05747291, 0.07340708, -0.067006536, -0.10147673,
                 -0.008331716, 0.05173064, 0.046279725, 0.03404632, 0.02740098, -0.083125755, 0.019780137, -0.083855614,
                 -0.009615373, 0.008593247, 0.017608564, -0.00038568504, 0.0050966055, -0.08244318, 0.07768936,
                 0.0004437095, 0.0075502056]}
    , {'id': 279903, 'entity': '/resource/Anne_Doherty',
       'embeddings': [0.17391227, -0.0019253542, 0.11195737, -0.0083204135, 0.14768882, 0.06127454, -0.17685167,
                      -0.2456707, -0.019983718, 0.20017327, 0.15459292, 0.042724885, 0.032419465, -0.1343682,
                      0.16954385, -0.21044329, -0.068309605, 0.03422378, 0.0018794677, 0.023451317, -0.03977083,
                      -0.20629059, 0.13623942, 0.10686743, -0.008804895]},
 {'id': 488904, 'entity': '/resource/Boeing_747_hull_losses',
  'embeddings': [0.02233588, 0.010766734, 0.02364266, -0.027576402, 0.07801491, 0.042783223, -0.07689947, -0.079958074,
                 -0.047613777, 0.07463854, 0.01335002, 0.090599485, 0.011700771, -0.07999231, 0.011721943, -0.08457296,
                 -0.021597078, 0.011450011, -0.018370308, 0.007592149, 0.012584233, -0.10277818, 0.057296358,
                 -0.047838703, -0.008101291]}, {'id': 3754926, 'entity': '/resource/The_Troll%27s_Daughter',
                                                'embeddings': [0.051717333, 0.029857269, 0.025789587, -0.0052701286,
                                                               0.06531655, 0.056815453, -0.067051984, -0.09114491,
                                                               -0.052302763, 0.065642804, 0.06306678, 0.018283539,
                                                               0.05067654, -0.05543097, 0.056476004, -0.09056541,
                                                               0.0030044757, 0.050565034, 0.040417768, 0.036873262,
                                                               -0.007310663, -0.0727356, 0.033937242, 0.021133214,
                                                               0.028034253]},
 {'id': 74079, 'entity': '/resource/1995_in_Northern_Ireland',
  'embeddings': [0.042135652, 0.005255483, 0.07820453, -0.053622056, 0.079243734, 0.10314841, -0.08227035, -0.105380304,
                 -0.035254095, 0.085996285, 0.082117625, 0.06464705, 0.086902834, -0.1378, 0.070479825, -0.074492134,
                 0.007210387, -0.010879741, -0.0108703, 0.044665255, -0.003010596, -0.09002452, 0.13983987, -0.12688793,
                 0.03237472]},
 {'id': 2645499, 'entity': '/resource/Manuel_Garc%C3%ADa-Prieto%2C_1st_Marquis_of_Alhucemas',
  'embeddings': [0.04312162, 0.11208123, 0.15963256, -0.07783255, 0.17841083, 0.0190893, -0.08291694, -0.23706883,
                 -0.0060928604, 0.12571812, 0.08924673, 0.07373826, 0.08231033, -0.18005195, 0.09729942, -0.17233774,
                 -0.08608516, -6.638214e-05, 0.019301277, 0.02445094, 0.019734219, -0.112623386, 0.07493526,
                 -0.020603206, 0.0029067174]}, {'id': 3069345, 'entity': '/resource/Pelayo_Rodr%C3%ADguez_%28bishop%29',
                                                'embeddings': [0.071814984, 0.01424463, 0.03790827, -0.023001026,
                                                               0.1075073, 0.14349265, -0.0619078, -0.12683988,
                                                               -0.09711583, 0.053784028, 0.034007203, 0.059714977,
                                                               0.035672944, -0.099962264, 0.090515144, -0.087489806,
                                                               0.01003262, 0.008565291, -0.034069173, -0.009045737,
                                                               0.05428323, -0.07257777, 0.081728786, -0.003121235,
                                                               0.0060470435]},
 {'id': 1504388, 'entity': '/resource/Donjek_Glacier',
  'embeddings': [0.042226087, -0.0040272707, 0.030689815, -0.051381275, 0.14648798, 0.019058373, -0.12181891,
                 -0.15398708, -0.023053078, 0.059192646, 0.018359905, 0.0745518, 0.07532561, -0.11035549, 0.04459394,
                 -0.14049356, 0.0299517, 0.04064846, 0.0076664505, 0.02185194, 0.0024510152, -0.047114853, 0.10761586,
                 0.049493454, 0.034863167]}, {'id': 3361472, 'entity': '/resource/SMS_Strassburg',
                                              'embeddings': [0.13494651, 0.037904106, 0.03087857, -0.021026094,
                                                             0.107769705, 0.09956534, -0.21497463, -0.2124995,
                                                             -0.09889169, -0.042367566, 0.11011431, 0.12729916,
                                                             0.12641601, -0.2229637, -0.014506175, -0.13581042,
                                                             0.041774314, -0.03326853, 0.023415785, -0.00887427,
                                                             -0.0141287185, -0.22933494, 0.28636304, -0.04226652,
                                                             0.031803727]},
 {'id': 1991767, 'entity': '/resource/Hood%27s_Minstrels',
  'embeddings': [0.06376262, 0.082387224, 0.06823543, -0.01654788, 0.10578449, 0.054955173, -0.08456481, -0.13737132,
                 -0.08710622, 0.07085525, 0.052129608, 0.07608403, 0.0580844, -0.042735633, 0.07496751, -0.096754916,
                 -0.015868118, -0.0053665913, 0.029462248, 0.015160373, 0.047591202, -0.08630387, 0.120809056,
                 -0.013803998, 0.053700287]}]

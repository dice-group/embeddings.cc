import dask.dataframe as dd
from elasticsearch import Elasticsearch
es = Elasticsearch(["http://localhost:9200"])

def create_entity_index():
    index_config = {
        "settings": {
            "number_of_shards": 5,
            "number_of_replicas": 1
        },
        'mappings': {
            'properties': {
                'id': {
                    'type': 'keyword'
                },
                'entity': {
                    'type': 'keyword'
                },
                'embeddings': {
                    'type': 'dense_vector',
                    'dims': 25
                }

            }
        }
    }
    res = es.indices.create("shallom_dbpedia_index", body=index_config)
    print("Done")

create_entity_index()
data = dd.read_csv("Shallom_entity_embeddings.csv")
count = 0
doc_id = 0
documents = []
print("*********************************************")
print("Starting to index the relation embeddings now!!")
print("*********************************************")
for index, row in data.iterrows() :
    embeddings = row.to_list()[1:26]
    entity = row.to_list()[0]

    documents.append({
                "index": {
                    "_id": doc_id,
                    "_index": "shallom_dbpedia_index"
                }
            })
    documents.append({
        "id": doc_id,
        "entity": entity,
        "embeddings": embeddings
    })
    doc_id += 1
    if len(documents) == 100000:
        res = es.bulk(index="shallom_dbpedia_index", body=documents)
        count += 50000
        print(count)
        documents = []


import dask.dataframe as dd
from elasticsearch import Elasticsearch
es = Elasticsearch(["http://localhost:9200"])

index_name = "TransE_dbpedia_entity"
data_path  = "/data/KGE/TransE/entity_embeddings_dbp21-03_transe_dot.tsv"
dim = 100

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
                    'dims': dim
                }

            }
        }
    }
    res = es.indices.create(index_name, body=index_config)
    print("Done")

create_entity_index()
data = dd.read_csv(data_path, sep="\t")
count = 0
doc_id = 0
documents = []
print("*********************************************")
print("Starting to index the relation embeddings now!!")
print("*********************************************")
print(data.head())
for index, row in data.iterrows() :
    embeddings = row[1:dim+1]
    entity = row[0]
    documents.append({
                "index": {
                    "_id": doc_id,
                    "_index": index_name
                }
            })
    documents.append({
        "id": doc_id,
        "entity": entity,
        "embeddings": embeddings
    })
    doc_id += 1
    if len(documents) == 100000:
        res = es.bulk(index=index_name, body=documents)
        count += 50000
        print(count)
        documents = []
res = es.bulk(index=index_name, body=documents)

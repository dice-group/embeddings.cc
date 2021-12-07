from dask.distributed import Client
import dask.dataframe as dd
from elasticsearch import Elasticsearch
from jproperties import Properties

configs = Properties()
with open('app.props', 'rb') as config_file:
    configs.load(config_file)
es = Elasticsearch(["http://nel.cs.upb.de:9200"],
                   http_auth=(configs.get("elastic.user").data, configs.get("elastic.password").data))


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
                    'dims': 100
                }
            }
        }
    }
    res = es.indices.create("embedding_index", body=index_config)
    print("Done")


def create_relation_index():
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
                'relation': {
                    'type': 'keyword'
                },
                'operator': {
                    'type': 'text'
                },
                'dtype': {
                    'type': 'text'
                },
                'embeddings': {
                    'type': 'dense_vector',
                    'dims': 50
                }
            }
        }
    }
    res = es.indices.create("relation_embedding_index", body=index_config)
    print("Done")


def index_entity_docs():
    data = dd.read_csv("../nel/embeddings/entity_embeddings.tsv", sep="\t")
    count = 0
    doc_id = 0
    documents = []
    print("*********************************************")
    print("Starting to index the entity embeddings now!!")
    print("*********************************************")
    for index, row in data.iterrows() :
        embeddings = [float(i) for i in row['entity_embeddings'].split(",")]
        entity = row['entity']
        documents.append({
            "index": {
                "_id": doc_id,
                "_index": "embedding_index"
            }
        })
        documents.append({
            "id": doc_id,
            "entity": entity,
            "embeddings": embeddings
        })
        doc_id += 1
        if len(documents) == 100000:
            es.bulk(index="embedding_index", body=documents)
            count += 50000
            print(count)
            documents = []
    es.bulk(index="embedding_index", body=documents)
    print(doc_id)
    print("*********************************************")
    print("DONE!!")
    print("*********************************************")


def index_relation_docs():
    data = dd.read_csv("./relation_embeddings.tsv", sep="\t")
    count = 0
    doc_id = 0
    documents = []
    print("*********************************************")
    print("Starting to index the relation embeddings now!!")
    print("*********************************************")
    for index, row in data.iterrows() :
        embeddings = [float(i) for i in row['relation_embeddings'].split(",")]
        relation = row['relation']
        operator = row['operator']
        dtype = row['dtype']
        documents.append({
            "index": {
                "_id": doc_id,
                "_index": "relation_embedding_index"
            }
        })
        documents.append({
            "id": doc_id,
            "relation": relation,
            "embeddings": embeddings,
            "operator": operator,
            "dtype": dtype
        })
        doc_id += 1
        if len(documents) == 10000:
            es.bulk(index="relation_embedding_index", body=documents)
            count += 5000
            print(count)
            documents = []
    es.bulk(index="relation_embedding_index", body=documents)
    print(doc_id)
    print("*********************************************")
    print("DONE!!")
    print("*********************************************")


if __name__ == "__main__":
    client = Client()
    client
    # create_entity_index()
    # index_entity_docs()
    create_relation_index()
    index_relation_docs()

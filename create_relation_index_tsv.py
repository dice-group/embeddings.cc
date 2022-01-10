import dask.dataframe as dd
from elasticsearch import Elasticsearch
es = Elasticsearch(["http://localhost:9200"])

index_name = "transe_dbpedia_dot_relation"
data_path  = "/data/KGE/transe_dot/relation_types_parameters_dbp21-03_transe_dot.tsv"
dim = 100

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
                    'dims': dim
                }
            }
        }
    }
    res = es.indices.create(index_name, body=index_config)
    print("Done")
create_relation_index()

data = dd.read_csv(data_path, sep="\t")
count = 0
doc_id = 0
documents = []
print("*********************************************")
print("Starting to index the relation embeddings now!!")
print("*********************************************")
for index, row in data.iterrows() :
    row_list = list(row)
    embeddings = row_list[5:105]
    relation = row_list[0]
    operator = row_list[1]
    dtype = row_list[2]
    documents.append({
        "index": {
            "_id": doc_id,
            "_index": index_name
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
        es.bulk(index=index_name, body=documents)
        count += 5000
        print(count)
        documents = []
es.bulk(index=index_name, body=documents)
print(doc_id)
print("*********************************************")
print("DONE!!")
print("*********************************************")
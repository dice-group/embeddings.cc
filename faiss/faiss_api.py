import sys
import pickle
import faiss_indexers


def load_faiss_index(hnsw_appr, data_path, dataset_id, dimensions=300):
    if hnsw_appr:
        return faiss_indexers.load_HNSW_index(data_path+dataset_id+'.faiss_dense_appr', data_path+dataset_id+'.faiss_dense_appr_dict', dimensions)
    else:
        return faiss_indexers.load_Exact_index(data_path+dataset_id+'.faiss_dense', data_path+dataset_id+'.faiss_dense_dict')


def get_embeddings(faiss_index, entities):
    results = []
    for entity in entities:
        if entity in faiss_index.db_id_to_index_id:
            results.append((entity, faiss_index.getVectorForId(faiss_index.db_id_to_index_id[entity])))
    return results


def get_similar_embeddings(faiss_index, embeddings, number_of_results=10):
    results = []
    for i, result_uris in enumerate(faiss_index.search(embeddings, number_of_results)):
        for result_uri in result_uris:
            results.append((i, 0.5, result_uri))
            # TODO: 4th element (embeddings) missing
    return results


def get_similar_entities(faiss_index, embeddings, number_of_results=10):
    results = []
    for i, result_uris in enumerate(faiss_index.search(embeddings, number_of_results)):
        for result_uri in result_uris:
            results.append((i, 0.5, result_uri))
    return results

def test():
    data_path  = '../data/'  # local
    #data_path  = '/data/data_files/'  # VM

    dataset_id = 'example'  # (4 pairs)
    #dataset_id = 'dbpedia_en_fr_15k_procrustes'  # (30,000 pairs)
    #dataset_id = 'dbpedia_wikidata_full'  # (180 mio pairs)

    faiss_index = load_faiss_index(False, data_path, dataset_id)
    print()
    print('get_embeddings')
    print(get_embeddings(faiss_index, ['http://example.com/1']))
    print()
    print('get_similar_embeddings')
    print(get_similar_embeddings(faiss_index, [[0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0], [1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9, 0.0]], number_of_results=3))
    print()
    print('get_similar_entities')
    print(get_similar_entities(faiss_index, [[0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0], [1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9, 0.0]], number_of_results=3))

if False:
    test()

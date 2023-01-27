import sys
import numpy
sys.path.insert(1, '../api/serialization/')
from file_reader import FileReader
import pickle
import faiss
sys.path.insert(1, '../faiss_api/')
import faiss_api

# Download the data here:
# https://hobbitdata.informatik.uni-leipzig.de/embeddings_cc/data/dbpedia_en_fr_15k_procrustes.uris.txt.bz2
# https://hobbitdata.informatik.uni-leipzig.de/embeddings_cc/data/dbpedia_en_fr_15k_procrustes.embeddings.txt.bz2

# Set the local data path:
data_path = '/home/wilke/Data/embeddings_cc/data/'
#data_path = '../datatoindex/'

# Set data files:
if True:
    file_embs = 'dbpedia_en_fr_15k_procrustes.embeddings.txt.bz2' # (30,000 pairs)
    file_uris = 'dbpedia_en_fr_15k_procrustes.uris.txt.bz2'
else:
    file_embs = 'example.embeddings.txt.bz2' # (4 pairs)
    file_uris = 'example.uris.txt.bz2'

# Set approximation (or exact):
hnsw_appr = True

# Load data:
data = []
for item in FileReader(embeddings_file=data_path+file_embs, uri_file=data_path+file_embs, format='bzip2'):
    data.append((item[0], item[1]))
if False:
    print('Types:          ', type(data[0]), type(data[0][0]), type(data[0][1]), type(data[0][1][0]))
    print('Dimensions:     ', len(data[-1][1]))
    print('First item:     ', data[0])
    print('Last item:      ', data[-1])
print('Number of items:', len(data))

# Compute index
print("start indexing")
max_id = 0
x_dim = len(data)
y_dim = len(data[0][1])
if not hnsw_appr:
    index = faiss_api.DenseFlatIndex(vector_sz=y_dim)
else:
    #option2 two HNSW index -> approximate index
    index = faiss_api.DenseHNSWFlatIndex(vector_sz=y_dim)
vectors = numpy.zeros((x_dim, y_dim), dtype=numpy.float32)
for sample in data:
    vectors[max_id] = numpy.asarray(sample[1])
    index.index_id_to_db_id.update({max_id: sample[0]})
    max_id = max_id + 1
index.index_data(vectors)

# Save
if hnsw_appr:
    index_name="faiss_dense_appr"
else:
    index_name="faiss_dense"
id_to_index_name=index_name+"_dict.sav"

print(index.index.ntotal)
pickle.dump(index.index_id_to_db_id, open(id_to_index_name, 'wb'))
faiss.write_index(index.index, index_name)
print("finished")


# TODO: Create a Faiss index containing the data
# https://github.com/facebookresearch/faiss/wiki/Getting-started

# TODO: def get_embeddings()
# Input: Up to 100 entity-identifiers (URIs or indexes of entities)
# Output: Embeddings for the input

# TODO: get_similar_embeddings()
# Input: Up to 100 entity-identifiers (URIs or indexes of entities)
# Output: Top-10 most similar entries: Similarity-score, entity-identifier and embeddings

# TODO: get_similar_entities()
# Input: up to 100 embeddings (or indexes)
# Output: Top-10 most similar: Similarity-score and entity-identifier


# Creates Faiss index
# Requires: embeddings file and uris file
#
import sys
import numpy
import pickle
import faiss
import faiss_indexers
sys.path.insert(1, '../api/serialization/')
from file_reader import FileReader

# Set the local data path, files, and format:
data_path  = '../data/'  # local
#data_path  = '/data/data_files/'  # VM
dataset_id = 'example'  # (4 pairs)
#dataset_id = 'dbpedia_en_fr_15k_procrustes'  # (30,000 pairs)
#dataset_id = 'dbpedia_wikidata_full'  # (180 mio pairs)
#data_format='bzip2'
data_format='txt'
file_path_prefix = data_path + dataset_id

# Set approximation (or exact):
hnsw_appr = False

# Load data:
data = []
if data_format == 'txt':
    file_extension = '.txt'
else:
    file_extension = '.txt.bz2'
for item in FileReader(embeddings_file=file_path_prefix+'.embeddings'+file_extension, uri_file=file_path_prefix+'.uris'+file_extension, format=data_format):
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
    index = faiss_indexers.DenseFlatIndex(vector_sz=y_dim)
else:
    index = faiss_indexers.DenseHNSWFlatIndex(vector_sz=y_dim)
vectors = numpy.zeros((x_dim, y_dim), dtype=numpy.float32)
for sample in data:
    vectors[max_id] = numpy.asarray(sample[1])
    index.index_id_to_db_id.update({max_id: sample[0]})
    max_id = max_id + 1
index.index_data(vectors)

# Save
if hnsw_appr:
    index_name=file_path_prefix+'.faiss_dense_appr'
else:
    index_name=file_path_prefix+'.faiss_dense'
id_to_index_name=index_name+"_dict"
print(index.index.ntotal)
pickle.dump(index.index_id_to_db_id, open(id_to_index_name, 'wb'))
faiss.write_index(index.index, index_name)
print("finished")

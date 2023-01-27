import sys
sys.path.insert(1, '../faiss_api/')
import faiss_api
sys.path.insert(1, '../api/serialization/')
from file_reader import FileReader

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
hnsw_appr = False
    
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

if hnsw_appr:
    search_index=faiss_api.load_HNSW_index("faiss_dense_appr","faiss_dense_appr_dict.sav", 300)
else:
    search_index=faiss_api.load_Exact_index("faiss_dense","faiss_dense_dict.sav")

print(search_index.search([data[0][1]],5))
print()
print(search_index.getVectorForId(2))

from faiss_api import faiss_api
import sys
sys.path.insert(1, '../api/serialization/')
from file_reader import FileReader

data_path = '../datatoindex/'
# Load data (30,000 pairs):
data = []
for item in FileReader(embeddings_file=data_path+'dbpedia_en_fr_15k_procrustes.embeddings.txt.bz2', uri_file=data_path+'dbpedia_en_fr_15k_procrustes.uris.txt.bz2', format='bzip2'):
    data.append((item[0], item[1]))
print('Types:          ', type(data[0]), type(data[0][0]), type(data[0][1]), type(data[0][1][0]))
print('Dimensions:     ', len(data[-1][1]))
print('First item:     ', data[0])
print('Last item:      ', data[-1])
print('Number of items:', len(data))

search_index=faiss_api.load_Exact_index("faiss_dense","faiss_dense_dict.sav")
#sv=data[0][1]
#res=search_index.search([data[0][1]],5)
print(search_index.getVectorForId(2))

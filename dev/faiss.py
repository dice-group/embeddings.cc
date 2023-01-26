import sys

sys.path.insert(1, '../api/serialization/')
from file_reader import FileReader

# Download the data here:
# https://hobbitdata.informatik.uni-leipzig.de/embeddings_cc/data/dbpedia_en_fr_15k_procrustes.uris.txt.bz2
# https://hobbitdata.informatik.uni-leipzig.de/embeddings_cc/data/dbpedia_en_fr_15k_procrustes.embeddings.txt.bz2

# Set the local data path:
data_path = '/home/wilke/Data/embeddings_cc/data/'

# Load data (30,000 pairs):
data = []
for item in FileReader(embeddings_file=data_path+'dbpedia_en_fr_15k_procrustes.embeddings.txt.bz2', uri_file=data_path+'dbpedia_en_fr_15k_procrustes.uris.txt.bz2', format='bzip2'):
    data.append((item[0], item[1]))
print('Types:          ', type(data[0]), type(data[0][0]), type(data[0][1]), type(data[0][1][0]))
print('Dimensions:     ', len(data[-1][1]))
print('First item:     ', data[0])
print('Last item:      ', data[-1])
print('Number of items:', len(data))

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


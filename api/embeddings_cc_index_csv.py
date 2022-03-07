# CSV example for embeddings.cc index API
# https://github.com/dice-group/embeddings.cc
#
# Usage:       time python3 api/embeddings_cc_index_csv.py <PASSWORD>
# Local usage: time python3 api/embeddings_cc_index_csv.py <PASSWORD> http://127.0.0.1:8008
#
# Local runtime for 200k: 10m56,588s -> 32.85 seconds for 10,000 entries.

import sys
import csv
from embeddings_cc_index import EmbeddingsCcIndex

# Configuration
# Original data: https://github.com/nju-websoft/OpenEA#dataset-overview
# Shallom data: https://hobbitdata.informatik.uni-leipzig.de/KGE/OpenEA_V1.1_DBpedia_EN_FR_100K/V1/Shallom_10_300.zip
csv_file = '/tmp/Shallom_10_300/Shallom_entity_embeddings.csv'
es_index = 'openea_v1.1_dbpedia_en_fr_100k_v1_shallom_10_300___'
dimensions = 300

# Get password form CLI
if len(sys.argv) > 1:
    password = sys.argv[1]
else:
    print('Please provide a password')
    sys.exit(1)

# Get webservice URL form CLI
webservice_url = None
if len(sys.argv) > 2:
    webservice_url = sys.argv[2]

print("csv_file:", csv_file)
print("es_index:", es_index)
print("dimensions:", dimensions)
print("webservice_url:", webservice_url)

# Create instance
embeddings_cc_index = EmbeddingsCcIndex(webservice_url=webservice_url)

# Delete index
response = embeddings_cc_index.delete_index(password, es_index)
print(response.status_code, response.text)

# Create index
response = embeddings_cc_index.create_index(password, es_index, dimensions, shards=5)
print(response.status_code, response.text)


# Add data
def add_embeddings(api, password, index, embeddings):
    response = api.add(password, index, embeddings)
    if response.status_code == 200:
        print(i, end=' ')
        sys.stdout.flush()
        return True
    else:
        print(response.status_code, response.text)
        return False


# Parse CSV
with open(csv_file, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')

    # Skip header / first line
    next(reader)

    embeddings = []
    for i, row in enumerate(reader):
        numeric_array = [float(numeric_string) for numeric_string in row[1:]]
        embeddings.append([row[0], numeric_array])

        # Add data
        if i % 5000 == 0:
            if not add_embeddings(embeddings_cc_index, password, es_index, embeddings):
                break
            embeddings = []

    # Add data
    if len(embeddings) > 0:
        add_embeddings(embeddings_cc_index, password, es_index, embeddings)
    print("Number of datasets:", i+1)

    # Print number of documents
    response = embeddings_cc_index.count(es_index)
    print(response.status_code, response.text)

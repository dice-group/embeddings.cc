# Examples for embeddings.cc index API
# https://github.com/dice-group/embeddings.cc
#
# Usage:       python3 api/embeddings_cc_index_examples.py <PASSWORD>
# Local usage: python3 api/embeddings_cc_index_examples.py <PASSWORD> http://127.0.0.1:8008

import sys
import ast
from embeddings_cc_index import EmbeddingsCcIndex

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

# Create instance
embeddings_cc_index = EmbeddingsCcIndex(webservice_url=webservice_url)

# ----------| GET requests without password |---------------------------------------------------------------------------

# Ping webservice
if True:
    statusCode = embeddings_cc_index.ping(seconds=1)
    if statusCode == 502:
        print('502: Webservice unavailable')
        sys.exit(1)
    elif statusCode == 503:
        print('503: Elasticsearch service unavailable')
        sys.exit(1)
    else:
        print(statusCode)

# Returns number of documents in Elasticsearch index.
if False:
    response = embeddings_cc_index.count('index_test')
    print(response.status_code, response.text)

# Searches for an entity in Elasticsearch and returns related embeddings.
if False:
    response = embeddings_cc_index.get_embeddings('index_test', 'http://example.com/0')
    print(response.status_code, response.text)

# ----------| POST requests with password |-----------------------------------------------------------------------------

# Returns webservice response containing existing Elasticsearch indexes.
if True:
    response = embeddings_cc_index.get_indexes(password)
    print(response.status_code, response.text)

# Creates an Elasticsearch index and returns Elasticsearch API response.
if False:
    response = embeddings_cc_index.create_index(password, 'index_test', 10, shards=5)
    print(response.status_code, response.text)

# Deletes an Elasticsearch index and returns Elasticsearch API response.
if False:
    response = embeddings_cc_index.delete_index(password, 'index_test')
    print(response.status_code, response.text)

# Adds data.
# Data is transformed to JSON, so tuples and lists are handled equally.
# Important: Split your data into multiple requests and wait for a response
# before adding additional data. A request can take max 50,000 items.
if False:
    embeddings = [('http://example.com/0', [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]),
                  ('http://example.com/1', [1, 2, 3, 4, 5, 6, 7, 8, 9, 0])]
    print(embeddings)
    response = embeddings_cc_index.add(password, 'index_test', embeddings)
    print(response.status_code, response.text)
if False:
    embeddings = [['http://example.com/2', [2, 3, 4, 5, 6, 7, 8, 9, 0, 1]],
                  ['http://example.com/3', [3, 4, 5, 6, 7, 8, 9, 0, 1, 2]]]
    print(embeddings)
    response = embeddings_cc_index.add(password, 'index_test', embeddings)
    print(response.status_code, response.text)

# Add data of a CSV file
#
# Data: https://hobbitdata.informatik.uni-leipzig.de/KGE/DBpedia_EN_FR_15K/V2/Shallom.zip
# Line format: http://dbpedia.org/resource/E734345,0.4001125,[...],-0.015108802
#
# Note: Adding 1,000 embeddings takes around 15 seconds
# time python3 api/embeddings_cc_index_examples.py <PASSWORD>                -> 7m47,509s (Reading/parsing: ~33s)
# time python3 api/embeddings_cc_index_examples.py 123 http://127.0.0.1:8008 -> 2m10,133s
if False:
    csv_file = '/tmp/Shallom_entity_embeddings.csv'
    es_index = 'dbpedia_en_fr_15k_v2_shallom___'
    max_docs = 100 * 1000

    # Delete index
    response = embeddings_cc_index.delete_index(password, es_index)
    print(response.status_code, response.text)

    # Create index
    response = embeddings_cc_index.create_index(password, es_index, 300, shards=5)
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

    with open(csv_file) as file:
        embeddings = []
        for i, line in enumerate(file):
            # Skip first line
            if i == 0:
                continue
            # Limit to max number of documents
            elif i == max_docs:
                break
            # Remove new line character and split by first comma
            data = line.rstrip('\n').split(',', 1)
            # Print dimensions
            if i == 1:
                print('Dimensions:', data[1].count(',') + 1)
            # Collect data
            embeddings.append([data[0], ast.literal_eval('[' + data[1] + ']')])
            # Add data
            if i % 5000 == 0:
                if not add_embeddings(embeddings_cc_index, password, es_index, embeddings):
                    break
                embeddings = []
        # Add data
        if len(embeddings) > 0:
            add_embeddings(embeddings_cc_index, password, es_index, embeddings)
        print("Number of datasets:", i)

    # Print number of documents
    response = embeddings_cc_index.count(es_index)
    print(response.status_code, response.text)

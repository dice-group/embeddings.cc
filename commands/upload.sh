#!/bin/bash
echo "Upload embeddings..."
eval "$(conda shell.bash hook)"
conda activate embcc
python api/embeddings_cc_index_upload.py "EasyPass"  http://127.0.0.1:8008 ./embeddings/*_entity_embeddings.csv
python api/embeddings_cc_index_upload.py "EasyPass"  http://127.0.0.1:8008 ./embeddings/*_relation_embeddings.csv

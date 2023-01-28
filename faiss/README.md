# Faiss extension

## 1. Provide data

- Use the [Backup ES Index script](../scripts/backup-es-index.py) to get data from ES or
- Store an embeddings file and a URIs file in a data directory (e.g. `/data/data_files/`) for the next step.

## 2. Create Faiss index

- Use [faiss_create_indices.py](faiss_create_indices.py) to create an index from the embeddings file.
This also creates an inverted-index from URI to faissID.

## 3. API methods

- Use [faiss_api.py](faiss_api.py) to request data.
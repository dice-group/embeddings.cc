#!/bin/bash

#echo "[Starting Elasticsearch]"
#sudo systemctl start elasticsearch.service

echo "[Info: Available embeddings]"
conda env list

echo "[Starting webservice public]"
eval "$(conda shell.bash hook)" # https://stackoverflow.com/a/56155771
conda activate embeddings8
export FLASK_APP=webservice_index
export FLASK_RUN_PORT=1338
export FLASK_DEBUG=True
flask run

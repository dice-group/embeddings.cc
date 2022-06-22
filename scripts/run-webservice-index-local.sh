#!/bin/bash

#echo "[Starting Elasticsearch]"
#sudo systemctl start elasticsearch.service

echo "[Starting webservice index]"
eval "$(conda shell.bash hook)" # https://stackoverflow.com/a/56155771
conda activate embeddings
conda env list
export FLASK_APP=webservice_index
export FLASK_RUN_PORT=8008
export FLASK_DEBUG=True
flask run

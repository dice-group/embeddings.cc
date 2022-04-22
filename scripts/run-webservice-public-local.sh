#!/bin/bash

#echo "Starting Elasticsearch"
#sudo systemctl start elasticsearch.service

echo "Available embeddings"
conda env list

echo "Starting webservice public"
eval "$(conda shell.bash hook)" # https://stackoverflow.com/a/56155771
conda activate embeddings8
export FLASK_APP=webservice_public
export FLASK_RUN_PORT=1337
export FLASK_DEBUG=True
flask run

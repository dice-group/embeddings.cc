#!/usr/bin/bash -e
eval "$(conda shell.bash hook)"
echo "before calling source: $PATH"
conda create -n embcc python=3.10 --y
conda activate embcc
echo "after calling source: $PATH"
python -m pip install -r requirements.txt
mkdir -p instance
cp -f ./config.py instance
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.3.3-linux-x86_64.tar.gz
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.3.3-linux-x86_64.tar.gz.sha512
shasum -a 512 -c elasticsearch-8.3.3-linux-x86_64.tar.gz.sha512 
tar -xzf elasticsearch-8.3.3-linux-x86_64.tar.gz

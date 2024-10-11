#!/usr/bin/bash -e
eval "$(conda shell.bash hook)"
echo "before calling source: $PATH"
git clone https://github.com/dice-group/embeddings.cc.git && cd embeddings.cc
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
wget https://files.dice-research.org/datasets/dice-embeddings/KGs.zip --no-check-certificate && unzip KGs.zip && rm -rf KGs.zip
dicee --dataset_dir KGs/UMLS --model DeCaL --num_epochs 1 --batch_size 512 --path_to_store_single_run ./embeddings --save_embeddings_as_csv --eval_model "None" --embedding_dim 64

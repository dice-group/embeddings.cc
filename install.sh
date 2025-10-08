#!/usr/bin/bash -e
eval "$(/Users/admin/miniconda3/bin/conda shell.zsh hook)" # echo "before calling source: $PATH"
# git clone https://github.com/dice-group/embeddings.cc.git && cd embeddings.cc
ml lang
ml Miniforge3
conda create -n embcc python=3.10 -y
conda init
. $HOME/.bashrc
conda activate /Users/admin/miniconda3/envs/embcc
python -m pip install -r requirements.txt
mkdir -p instance
cp -f ./config.py instance
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.3.3-linux-x86_64.tar.gz
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.3.3-linux-x86_64.tar.gz.sha512
shasum -a 512 -c elasticsearch-8.3.3-linux-x86_64.tar.gz.sha512 
tar -xzf elasticsearch-8.3.3-linux-x86_64.tar.gz
# wget https://files.dice-research.org/datasets/dice-embeddings/KGs.zip --no-check-certificate && unzip KGs.zip && rm -rf KGs.zip
# dicee --dataset_dir KGs/UMLS --model DeCaL --num_epochs 1 --batch_size 512 --path_to_store_single_run ./embeddings --save_embeddings_as_csv --eval_model "None" --embedding_dim 64

/scratch/hpc-prf-whale/albert/uploader_embeddings/embeddings.cc/.conda/envs/embcc/bin/python /scratch/hpc-prf-whale/albert/uploader_embeddings/embeddings.cc/api/embeddings_cc_index_upload.py 'uni_kgs_emb_index' /scratch/hpc-prf-whale/albert/uploader_embeddings/data/Keci_GPU_wikizero.org.txt/embeddings.csv
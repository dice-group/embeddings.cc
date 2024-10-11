#!/usr/bin/bash -e
eval "$(conda shell.bash hook)"
conda activate embcc
dicee --dataset_dir data/ --model DeCaL --num_epochs 1 --batch_size 512 --path_to_store_single_run ./embeddings --save_embeddings_as_csv --eval_model "None"

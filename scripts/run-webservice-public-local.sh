#!/bin/bash -e

echo "[Starting webservice public]"
eval "$(/Users/admin/miniconda3/bin/conda shell.zsh hook)"
conda activate /Users/admin/miniconda3/envs/embcc
export FLASK_APP=webservice_public
export FLASK_RUN_PORT=1337
export FLASK_DEBUG=True
flask run
#flask run --host=0.0.0.0

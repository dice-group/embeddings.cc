#!/usr/bin/bash -e

echo "[Starting webservice public]"
eval "$(conda shell.bash hook)" # https://stackoverflow.com/a/56155771
conda activate embcc
conda env list
export FLASK_APP=webservice_public
export FLASK_RUN_PORT=1337
export FLASK_DEBUG=True
flask run
#flask run --host=0.0.0.0

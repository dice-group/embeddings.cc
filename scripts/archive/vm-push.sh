#!/bin/bash

# To be executed in parent directory
if ! test -f "README.md"; then
    echo "README.md file not found in current directory. Canceling."
    exit
fi

rsync -aP --exclude={'instance','__pycache__','.*'} ./ wilke@embeddings.cs.uni-paderborn.de:/tmp/embeddings.cc

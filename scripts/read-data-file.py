#!/usr/bin/env python3

import bz2

# Configuration
file_embeddings = 'dbpedia_en_fr_15k_procrustes.embeddings.txt.bz2'
file_uris = 'dbpedia_en_fr_15k_procrustes.uris.txt.bz2'
use_bz2 = True

# Open file
if use_bz2:
    f_uris = bz2.open(file_uris, mode='rt', compresslevel=9, encoding=None, errors=None, newline=None)
    f_embs = bz2.open(file_embeddings, mode='rt', compresslevel=9, encoding=None, errors=None, newline=None)
else:
    f_uris = open(file_uris, 'r')
    f_embs = open(file_embeddings, 'r')

# Read
count = 0
while True:
    count += 1
    uri = f_uris.readline()
    emb = f_embs.readline()
    if count == 1:
        print(count, emb)
        print(count, uri)
    if not uri or not emb:
        count -= 1
        break
print(count)

# Finally close file
f_uris.close()
f_embs.close()

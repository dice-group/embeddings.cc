import os
# This file contains public configuration (do not insert passwords etc.)
# Copy this file into the 'instance' directory to enable usage.

# Elasticsearch
ES_HOST       = os.getenv('ES_HOST', '')
ES_USER       = os.getenv('ES_USER', '')
ES_PASSWORD   = os.getenv('ES_PASSWORD', '')

# demo db
ES_HOST_DEMO       = os.getenv('ES_HOST_DEMO', '')
ES_USER_DEMO       = os.getenv('ES_USER', '')
ES_PASSWORD_DEMO   = os.getenv('ES_PASSWORD', '')

#ES_INDEX      = 'index_test'
#ES_INDEX      = 'dbpedia_en_fr_100k_procrustes_v2'
#ES_INDEX      = 'dbpedia_en_fr_15k_procrustes'
#ES_INDEX      = 'dbpedia-wikidata-v1'
ES_INDEX      = 'dbpedia_wikidata_full'
# ES_INDEX     = 'whale'

# Webservice password.
# Generate with scripts/generate-salt-password.py
#python scripts/generate-salt-password.py uni_kgs_emb_index
SALT          = os.getenv('SALT', '')
PSW_SALT_HASH = os.getenv('PSW_SALT_HASH', '')
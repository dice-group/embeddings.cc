# This file contains public configuration (do not insert passwords etc.)
# Copy this file into the 'instance' directory to enable usage.

# Elasticsearch
ES_HOST       = 'https://localhost:9200/'
ES_USER       = 'elastic'
ES_PASSWORD   = 'x#n8bqhE@fMq$yIJ'
ES_INDEX      = 'index_example'

# Webservice password.
# Generate with scripts/generate-salt-password.py
SALT          = b'[\xbdr\x15\xc5\t\xa9t***\xdc-\xc3\xc2\xe9\xbe\xa7k)\n=\xc3\x94\x93\xe7\x15\xb80\xaf<V'
PSW_SALT_HASH = b'\x03\xea\x1b\x867Y\x95lf\xa3\x0f{o\xc2\xc27\xc8\xa4k\x01\x1d0\x07\xd7)\x07:\xc6\x0f\xb4\x8f\x1b'

# Webservice password '123123' for local tests
#SALT          = b'[\xbdr\x15\xc5\t\xa9t***\xdc-\xc3\xc2\xe9\xbe\xa7k)\n=\xc3\x94\x93\xe7\x15\xb80\xaf<V'
#PSW_SALT_HASH = b'\x03\xea\x1b\x867Y\x95lf\xa3\x0f{o\xc2\xc27\xc8\xa4k\x01\x1d0\x07\xd7)\x07:\xc6\x0f\xb4\x8f\x1b'

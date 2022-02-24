# This file contains public configuration (do not insert passwords etc.)
# Copy this file into the 'instance' directory to enable usage.

# Elasticsearch
ES_HOST     = 'http://localhost:9200/'
ES_USER     = 'elastic'
ES_PASSWORD = ''

# Password salt. generate with: print(os.urandom(32))
SALT = b'@\x16\xf8]OY\xdfGn\x81\xb2E/?\xeb\xd5\\ll\xb5\x9eUF\xb5\t\xfc\xfe"\xf4#T\xc3'

# SHA-256 of Password+Salt, see https://nitratine.net/blog/post/how-to-hash-passwords-in-python/
PSW_SALT_HASH = b'_1&\xd8\xb7f9\x10\xd0q\x80\x8a\x19\x8e\x03\xf6\xf2\x84\x90\xa5\xb5c+\xe4\x9d\x85\xf7\x0eT\x191\xe9'

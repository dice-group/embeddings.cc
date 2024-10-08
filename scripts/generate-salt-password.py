# Script to generate config.py values

import os
import json
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from webservice_index import security

if len(sys.argv) > 1:
    password = sys.argv[1]
else:
    print('Please provide a password')
    sys.exit(1)

salt = security.generate_salt()
hash_ = security.hash_password(password, salt)

with open("./salt_password.json", "w") as f:
    json.dump({"salt": str(salt), "psw": str(hash_)}, f)

print('SALT          =', salt)
print('PSW_SALT_HASH =', hash_)

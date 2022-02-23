# Code based on https://nitratine.net/blog/post/how-to-hash-passwords-in-python/

import os
import hashlib
from flask import current_app


def check_password(password):
    return current_app.config['PSW_SALT_HASH'] == hash_password(password, current_app.config['SALT'])


def hash_password(password, salt):
    return hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100000)


def generate_salt():
    return os.urandom(32)

# embeddings.cc index API
# https://github.com/dice-group/embeddings.cc

import httpx
import json


class EmbeddingsCcIndex():

    def __init__(self, webservice_url='http://127.0.0.1:5000/'):
        self.webservice_url = webservice_url
        self.headers_json = {'Content-Type': 'application/json'}

    def ping(self, seconds=1):
        try:
            return httpx.get(self.webservice_url + '/ping', timeout=seconds).status_code == 200
        except httpx.ConnectTimeout:
            return False

    def get_indexes(self, password):
        return httpx.post(self.webservice_url + '/get_indexes', params={'password':password})

    def create_index(self, password, index, dimensions, number_of_shards=5):
        return httpx.post(self.webservice_url + '/create_index', params={'password':password, 'index':index, 'dimensions':dimensions, 'number_of_shards':number_of_shards })

    def delete_index(self, password, index):
        return httpx.post(self.webservice_url + '/delete_index', params={'password':password, 'index':index})
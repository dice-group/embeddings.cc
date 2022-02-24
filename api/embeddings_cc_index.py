# embeddings.cc index API
# https://github.com/dice-group/embeddings.cc

import httpx
import json


class EmbeddingsCcIndex():
    WEBSERVICE_URL = 'http://embeddings.cs.uni-paderborn.de:8008'

    def __init__(self, webservice_url=None):
        if webservice_url is None:
            self.webservice_url = self.WEBSERVICE_URL
        else:
            self.webservice_url = webservice_url
        self.headers_json = {'Content-Type': 'application/json'}

    def ping(self, seconds=1):
        """
        Returns:
        200: Success
        502: Webservice unavailable
        503: Elasticsearch service unavailable
        """
        try:
            return httpx.get(self.webservice_url + '/ping', timeout=seconds).status_code
        except httpx.RequestError as exc:
            return 502

    def get_indexes(self, password):
        """
        Returns webservice response containing existing Elasticsearch indexes.
        """
        return httpx.post(self.webservice_url + '/get_indexes', params={'password': password})

    def create_index(self, password, index, dimensions, number_of_shards=5):
        """
        Creates an Elasticsearch index and returns Elasticsearch API response.
        """
        return httpx.post(self.webservice_url + '/create_index',
                          params={'password': password, 'index': index, 'dimensions': dimensions,
                                  'number_of_shards': number_of_shards})

    def delete_index(self, password, index):
        """
        Deletes an Elasticsearch index and returns Elasticsearch API response.
        """
        return httpx.post(self.webservice_url + '/delete_index', params={'password': password, 'index': index})

    def add(self, password, index, docs):
        """
        Adds embeddings.
        Data is transformed to JSON, so tuples and lists are handled equally.
        Important: Split your data into multiple requests and wait for a response
        before adding additional data. A request could take e.g. 50,000 items.
        """
        data = json.JSONEncoder().encode({'password': password, 'index': index, 'docs': docs})
        return httpx.post(self.webservice_url + '/add', data=data, headers=self.headers_json)

    def get_embeddings(self, index, entity):
        """
        Searches for an entity in Elasticsearch and returns related embeddings.
        """
        return httpx.get(self.webservice_url + '/get_embeddings', params={'index': index, 'entity': entity})

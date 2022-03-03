# Development

## Configuration

- Set up a local system similar to the [VM](vm.md).
- To start the components, use these commands:

```bash
# Start Elasticsearch
sudo systemctl start elasticsearch.service

# Start webservice (public)
conda activate unikge  # or another venv
export FLASK_APP=webservice_public
export FLASK_RUN_PORT=1337  # or another port
export FLASK_DEBUG=True
flask run

# Start webservice (index)
export FLASK_APP=webservice_index
export FLASK_RUN_PORT=8008  # or another port
```

## Python

### Elasticsearch Python (7.16.0)

- [Elasticsearch Python Client 7.16](https://www.elastic.co/guide/en/elasticsearch/client/python-api/7.16/index.html)
- [Python Elasticsearch Client v7.16.0](https://elasticsearch-py.readthedocs.io/en/v7.16.0/)

### Elasticsearch Python DSL (7.4.0)

- [Elasticsearch DSL v7.4.0](https://elasticsearch-dsl.readthedocs.io/en/v7.4.0/)

### Flask (1.1.4)

- [Flask 1.1.x](https://flask.palletsprojects.com/en/1.1.x/)
- [Flask 1.1.x API](https://flask.palletsprojects.com/en/1.1.x/api/)
- [Flask 1.1.x Deployment Options](https://flask.palletsprojects.com/en/1.1.x/deploying/)
- [Flask 1.1.x uWSGI](https://flask.palletsprojects.com/en/1.1.x/deploying/uwsgi/)
- [Flask 1.1.x Tutorial](https://flask.palletsprojects.com/en/1.1.x/tutorial/)
- [Flask 1.1.x Tutorial Application Setup](https://flask.palletsprojects.com/en/1.1.x/tutorial/factory/) (config)

### API

- [HTTPX - A next-generation HTTP client for Python](https://www.python-httpx.org/)
- [json - JSON encoder and decoder](https://docs.python.org/3/library/json.html)

## Elasticsearch

- [ES blog: Text similarity search with vector fields](https://www.elastic.co/blog/text-similarity-search-with-vectors-in-elasticsearch)
- [ES blog: How many shards should I have in my Elasticsearch cluster?](https://www.elastic.co/blog/how-many-shards-should-i-have-in-my-elasticsearch-cluster)
- [Elasticsearch Guide [7.16] » How to » Size your shards](https://www.elastic.co/guide/en/elasticsearch/reference/7.16/size-your-shards.html)
- [Elasticsearch Guide [7.16] » REST APIs](https://www.elastic.co/guide/en/elasticsearch/reference/7.16/rest-apis.html)
- [Elasticsearch Guide [7.16] » REST APIs » Document APIs](https://www.elastic.co/guide/en/elasticsearch/reference/7.16/docs.html)
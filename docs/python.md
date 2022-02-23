# Python development

## Elasticsearch (7.16.0)

- [Elasticsearch Python Client 7.16](https://www.elastic.co/guide/en/elasticsearch/client/python-api/7.16/index.html)
- [Python Elasticsearch Client v7.16.0](https://elasticsearch-py.readthedocs.io/en/v7.16.0/)

## Elasticsearch DSL (7.4.0)

- [Elasticsearch DSL v7.4.0](https://elasticsearch-dsl.readthedocs.io/en/v7.4.0/)

## Flask (1.1.4)

- [Flask 1.1.x API](https://flask.palletsprojects.com/en/1.1.x/api/)
- [Flask 1.1.x Tutorial](https://flask.palletsprojects.com/en/1.1.x/tutorial/)
    - [Application Setup](https://flask.palletsprojects.com/en/1.1.x/tutorial/factory/) (config)

## API

- [HTTPX - A next-generation HTTP client for Python](https://www.python-httpx.org/)
- [json - JSON encoder and decoder](https://docs.python.org/3/library/json.html)

## Start Elasticsearch

- `sudo systemctl start elasticsearch.service`
- [http://localhost:9200/_cat/indices](http://localhost:9200/_cat/indices)

## Start webservices

- Preparation: Copy [config.py](../config.py) to instance/config.py
- Start:  
  `export FLASK_APP=webservice_index`  
  `flask run`
- [http://localhost:5000/ping](http://localhost:5000/ping)
- [http://localhost:5000/get_indexes?password=](http://localhost:5000/get_indexes?password=)
- [http://localhost:5000/create_index?password=&index_name=&dimensions=&number_of_shards=5](http://localhost:5000/create_index?password=&index_name=&dimensions=&number_of_shards=5)
- [http://localhost:5000/delete_index?password=&index_name=](http://localhost:5000/delete_index?password=&index_name=)

## Misc

- [Issue Data creation webservice](https://github.com/dice-group/kg-embedding-service/issues/14)
    - Local ES Installation
    - Current files overview
    - Initial python setup
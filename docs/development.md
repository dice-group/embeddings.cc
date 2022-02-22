# Development

## Elasticsearch (7.16.0)

- [Elasticsearch Python Client 7.16](https://www.elastic.co/guide/en/elasticsearch/client/python-api/7.16/index.html)
- [Python Elasticsearch Client v7.16.0](https://elasticsearch-py.readthedocs.io/en/v7.16.0/)

## Elasticsearch DSL (7.4.0)

- [Elasticsearch DSL v7.4.0](https://elasticsearch-dsl.readthedocs.io/en/v7.4.0/)

## Flask (1.1.4)

- [Flask 1.1.x API](https://flask.palletsprojects.com/en/1.1.x/api/)
- [Flask 1.1.x Tutorial](https://flask.palletsprojects.com/en/1.1.x/tutorial/)
    - [Application Setup](https://flask.palletsprojects.com/en/1.1.x/tutorial/factory/) (config)

## Start Elasticsearch

- `sudo systemctl start elasticsearch.service`
- [http://localhost:9200/_cat/indices](http://localhost:9200/_cat/indices)

## Start webservices

- Start:  
  `export FLASK_APP=webservice_index`  
  `flask run`
- [http://localhost:5000/ping](http://localhost:5000/ping)
- [http://localhost:5000/get_indexes?password=](http://localhost:5000/get_indexes?password=)

## Misc

- [Issue Data creation webservice](https://github.com/dice-group/kg-embedding-service/issues/14)
    - Local ES Installation
    - Current files overview
    - Initial python setup
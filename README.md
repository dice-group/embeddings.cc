Note: This project was developed while working on the article ***Universal Knowledge Graph Embeddings*** (repository: [Universal_Embeddings]([https://github.com/dice-group/Universal_Embeddings], publication [link](https://dl.acm.org/doi/10.1145/3589335.3651978))).

# Universal Knowledge Graph Embeddings

This repository contains code to run [embeddings.cc](https://embeddings.cc/) and [embeddings.cs.upb.de](https://embeddings.cs.upb.de:8443/) ([also without TLS](http://embeddings.cs.uni-paderborn.de/)).


## Documentation


### Public API (for users)

- The API is documented at [embeddings.cc/api](https://embeddings.cc/api)
- Additional examples are provided in [Python examples](api/embeddings_cc_public_examples.py) and [JavaScript HTML form](api/embeddings_cc_public.htm)


### Index API (for data developers)

- Use the Index API to create Elasticsearch indexes and to **add data**.
- It is only available in UPB network (use **VPN**).
- It can easily accessed using the methods in [API python file](api/embeddings_cc_index.py).  
  Usage examples are provided in the files for [simple examples](api/embeddings_cc_index_examples.py),
  in the [adding CSV](api/embeddings_cc_index_csv.py) and
  in the [adding UniKGE data](api/embeddings_cc_index_unikge.py).
- **Important**: Create an alias for each index to be available in public. Only aliases can be accessed by webservices.

| Webservice             | Method | Parameters                          |
|------------------------|--------|-------------------------------------|
| /ping                  | GET    | -                                   |
| /count                 | GET    | index                               |
| /get_embeddings        | GET    | index, entity                       |
| /get_cpu_usage         | POST   | password                            |
| /get_indexes           | POST   | password                            |
| /create_index          | POST   | password, index, dimensions, shards |
| /create_index_usagelog | POST   | password                            |
| /delete_index          | POST   | password, index                     |
| /add                   | POST   | password, index, docs               |
| /alias_put             | POST   | password, index, alias              |
| /alias_delete          | POST   | password, index, alias              |


### Development (for python developers)

- [How to install on your system](docs/local.md)
- [Development](docs/development.md) (External documentation of integrated components)


### Virtual machine (for system administrators)

- [Virtual machine](docs/vm.md) (Installation and deployment)
- [VM nginx](docs/vm-nginx-certbot.md) (Webserver configuration)
- [Deployment](docs/deployment.md) (How to publish a new version)
- Note: This is an extension of [kg-embedding-service](https://github.com/dice-group/kg-embedding-service)

![components](docs/images/components.svg "components")

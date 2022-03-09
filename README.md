# Universal Knowledge Graph Embeddings

This repository contains code to run [embeddings.cc](https://embeddings.cc/) and [embeddings.cs.upb.de](https://embeddings.cs.upb.de:8443/).

## Documentation

### Hidden features

- 💀 Please do not tell anyone! This is top secret! 💀
- [https://embeddings.cc/?dev](https://embeddings.cc/?dev)
- [https://embeddings.cc/usage](https://embeddings.cc/usage)
- [https://embeddings.cc/news](https://embeddings.cc/news)

### Public API (for users)

- The API is documented at [embeddings.cc/api](https://embeddings.cc/api)
- Additional examples are provided in [Python examples](api/embeddings_cc_public_examples.py) and [JavaScript HTML form](api/embeddings_cc_public.htm)

### Index API (for universal embeddings developers)

- Use the Index API to create Elasticsearch indexes and to add data.
- The API is only available in UPB network (use VPN).
- The API can easily accessed via the [API python file](api/embeddings_cc_index.py).
- Usage examples are provided in the [examples python file](api/embeddings_cc_index_examples.py) and
  in the [CSV example python file](api/embeddings_cc_index_csv.py).

| Webservice      | Method | Parameters                          |
|-----------------|--------|-------------------------------------|
| /ping           | GET    | -                                   |
| /count          | GET    | index                               |
| /get_embeddings | GET    | index, entity                       |
| /get_indexes    | POST   | password                            |
| /create_index   | POST   | password, index, dimensions, shards |
| /delete_index   | POST   | password, index                     |
| /add            | POST   | password, index, docs               |

### System administration

- [Virtual machine](docs/vm.md) (Installation and deployment)
- [VM nginx](docs/vm-nginx-certbot.md) (webserver configuration)
- [Development](docs/development.md) (Used python modules)
- Note: This is an extension of [kg-embedding-service](https://github.com/dice-group/kg-embedding-service)

![components](docs/images/components.svg "components")

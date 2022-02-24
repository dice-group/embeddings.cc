# Universal Knowledge Graph Embeddings

This repository contains code to run embeddings.cc

## Documentation

### Index API (for universal embeddings developers)

- Use the Index API to create Elasticsearch indexes and to add data.
- The API is only available in UPB network (use VPN).
- The API can easily accessed via a [python file](api/embeddings_cc_index.py).
- Usage examples are provided in an [example python file](api/embeddings_cc_index_examples.py).
- To check, if the webservice and Elasticsearch are running, use the [ping webservice](http://embeddings.cs.uni-paderborn.de:8008/ping).

### System administration

- [Virtual machine](docs/vm.md) (Installation instructions)
- [Python development](docs/python.md) (Used python modules)
- Note: This is an extension of [kg-embedding-service](https://github.com/dice-group/kg-embedding-service). Additional code can be found there.

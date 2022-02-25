# Universal Knowledge Graph Embeddings

This repository contains code to run embeddings.cc and [embeddings.cs.upb.de](http://embeddings.cs.upb.de:8443/)

## Documentation

### Public API (for users)

- [/api/v1/ping](http://embeddings.cs.upb.de:8443/api/v1/ping)
    - Returns 200 if the system is running
- [/api/v1/get_entities](http://embeddings.cs.upb.de:8443/api/v1/get_entities)
    - Returns up to 10 entities
- [/api/v1/get_embedding](http://embeddings.cs.upb.de:8443/api/v1/get_embedding?entity=http%3A%2F%2Fexample.com%2F0)
    - Parameter: entity
    - Returns embedding
- [/api/v1/get_similar](http://embeddings.cs.upb.de:8443/api/v1/get_similar?embedding=[0,1,2,3,4,5,6,7,8,9])
    - Parameter: embedding
    - Returns similar embeddings

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

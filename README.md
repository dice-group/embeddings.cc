Note: This project was developed while working on the article ***Universal Knowledge Graph Embeddings*** (repository: ([https://github.com/dice-group/Universal_Embeddings], publication [link](https://dl.acm.org/doi/10.1145/3589335.3651978))).

# Universal Knowledge Graph Embeddings

This repository contains code to run [embeddings.cc](https://embeddings.cc/) and [embeddings.cs.upb.de](https://embeddings.cs.upb.de:8443/) ([also without TLS](http://embeddings.cs.uni-paderborn.de/)).


## Documentation


### Public API (for users)

- The API is documented at [embeddings.cc/api](https://embeddings.cc/api)
- Additional examples are provided in [Python examples](api/embeddings_cc_public_examples.py) and [JavaScript HTML form](api/embeddings_cc_public.htm)


### Index API (for data developers)

#### Quick start for Linux
1. Make sure you have a csv file containing embeddings for entities. Entity names should be on the first column so that `pandas.read_csv("file_name.csv", index_col=0)` can run properly. Otherwise, please edit the script `api/embeddings_cc_index_upload.py` to fit your input file requirements.

2. Shell (Install Elasticsearch)
```shell
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.3.3-linux-x86_64.tar.gz
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.3.3-linux-x86_64.tar.gz.sha512
shasum -a 512 -c elasticsearch-8.3.3-linux-x86_64.tar.gz.sha512 
tar -xzf elasticsearch-8.3.3-linux-x86_64.tar.gz
cd elasticsearch-8.3.3 && ./bin/elasticsearch
```
3. You now have to set a password for the username (write down the password somewhere!). Open a new terminal. Run `cd elasticsearch-8.3.3 && ./bin/elasticsearch-reset-password --username elastic --interactive`. Follow instructions to set a new password.

4. Open a new terminal!
```python
python create -n embcc --y && conda activate embcc
git clone https://github.com/dice-group/embeddings.cc.git && cd embeddings.cc && pip install -r requirements.txt
mkdir instance && cp -f config.py instance/
```
5. Run `python scripts/generate-salt-password.py <PASSWORD>`. Note that `PASSWORD` must be the you created in step 3. Here you will get two outputs: values for `SALT` and `PSW_SALT_HASH`. Copy them to a safe place for the next step.
6. Edit the file `config.py` which is located in `embeddings_cc/instance`. ES_USER is `elastic` by default if you did not change it in the previous steps. ES_HOST is `https://localhost:9200/`. ES_PASSWORD is the password in step 7. ES_INDEX is the index you are willing to create (in our example, the index is "index_vicodi" as can be seen in the config file. If you use a different index name, make sure you use it in both `/instance/config.py` and `api/embeddings_cc_index_upload.py`). Set values for `SALT` and `PSW_SALT_HASH` as generated in step 5.
7. Open a new terminal and run `/scripts/run-webservice-public-local.sh`
8. Open another terminal and run `./scripts/run-webservice-index-local.sh`
9. Run `python api/embeddings_cc_index_upload.py <PASSWORD>  http://127.0.0.1:8008 PATH_CSV_FILE` (to upload your embeddings)
10. Now access the URL [http://127.0.0.1:1337/](http://127.0.0.1:1337/) to access the embeddings_cc API with your uploaded embeddings.

### Complete documentation
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

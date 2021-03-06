# Local installation

## Set up Elasticsearch

- Note: In the next steps. you have to collect the values for Elasticsearch *host*, *user* and *password*.
This project requires the configuration values to be availabe in [config.py](../config.py).
  When you finally open a host address like [https://localhost:9200/](https://localhost:9200/) and have to provide a user and password, you have prepared everything in this step.
- Install and/or start Elasticsearch on your machine
    - We currently use Elasticsearch version 8.3.1.
      Later versions will probably also work.
    - Download Elasticsearch from [elastic.co/downloads/elasticsearch](https://www.elastic.co/downloads/elasticsearch).
      For linux, check the [guide to download and install archive for Linux](https://www.elastic.co/guide/en/elasticsearch/reference/8.3/targz.html#install-linux).
    - See detailed instructions in the [Elasticsearch Guide](https://www.elastic.co/guide/en/elasticsearch/reference/8.3/index.html), part *Set up Elasticsearch*.
- Provide a password for the user *elastic*.
    - You can use the command `./bin/elasticsearch-reset-password --username elastic --interactive`.
    - The command is documented here: [elasticsearch-reset-password](https://www.elastic.co/guide/en/elasticsearch/reference/8.1/reset-password.html).
- You should be able to access [https://127.0.0.1:9200/](https://127.0.0.1:9200/).

## Install Python modules

- We recommend to use [Anaconda](https://www.anaconda.com/).
- Create an environment and install the required python modules by using these commands:
    - `conda create --name embeddings`
    - `conda activate embeddings`
    - `conda install -c conda-forge --file requirements.txt`

## Basic configuration

- Get the code of the [embeddings.cc repository](https://github.com/dice-group/embeddings.cc) (clone or download the code).
- Create a directory *instance* and copy the file [config.py](../config.py) into it. The final path should be *embeddings.cc/instance/config.py*
- Edit the file config.py.
    - Set *ES_HOST*, *ES_USER* and *ES_PASSWORD* from the previous step.
    - For *ES_INDEX*, you can use the value `'index_test'`.
    - To get the values for *SALT* and *PSW_SALT_HASH*, execute the script [generate-salt-password.py](../scripts/generate-salt-password.py).
      The plain password you provide here is required later to create an Elasticsearch index. The script can be executed using the command `python scripts/generate-salt-password.py <PASSWORD>`
- Run the commands in the script file [run-webservice-public-local.sh](../scripts/run-webservice-public-local.sh).
  Run this script from the root directory, e.g. ./scripts/run-webservice-public-local.sh. 
  (You may have to edit the commands to match your local configuration.)
- If you open [127.0.0.1:1337](http://127.0.0.1:1337/) now, there should be an error message stating that an index was not found.
  That is fine as we did not add any data.

## Create an Elasticsearch index

- Run the commands in the script file [run-webservice-index-local.sh](../scripts/run-webservice-index-local.sh) to start the webservice for adding data.
  Run this script from the root directory, e.g. ./scripts/run-webservice-index-local.sh. 
  (You may have to edit the commands to match your local configuration.)
  Opening [http://127.0.0.1:8008/ping](http://127.0.0.1:8008/ping) should return Status: OK.
- Edit the file [embeddings_cc_index_examples.py](../api/embeddings_cc_index_examples.py)
    - Set *do_create_index*, *do_create_index_usagelog*, *do_alias_put* and *do_add_data_list* to *True*.
    - Execute `python api/embeddings_cc_index_examples.py <PASSWORD> http://127.0.0.1:8008`
    - You should get several HTTP return codes 200.

## System check

- You can stop the script `run-webservice-index-local.sh`, e.g. by pressing CTRL+C.
- Run the commands in the script file [run-webservice-public-local.sh](../scripts/run-webservice-public-local.sh).
  (You may have to edit the commands to match your local configuration.)
- If you open [127.0.0.1:1337](http://127.0.0.1:1337/) now, the embeddings.cc frontend should be visible.

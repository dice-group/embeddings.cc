# Deployment

The current deployment uses the existing VM configuration and basically is  
(a) downloading the current version from GitHub,  
(b) creating a link to /opt/config.py and  
(c) linking from /opt/embeddings.

- Login
    - `kinit wilke`  
      (or another upb user)
    - `ssh wilke@embeddings.cs.upb.de`
- Source code to /opt
    - `emb=/opt/embeddings.cc-2022-06-30`  
      (or another directory)
    - `cd /tmp`
    - `wget https://github.com/dice-group/embeddings.cc/archive/refs/heads/master.zip`
    - `unzip master.zip ; rm master.zip`
    - `mv embeddings.cc-master $emb`
- Link config
    - `cd $emb`
    - `mkdir instance`
    - `ln -s /opt/config.py instance/`
- Link new instance
    - `sudo systemctl stop embeddings.service`
    - `unlink /opt/embeddings`
    - `ln -s $emb /opt/embeddings`
    - `sudo systemctl start embeddings.service`
- Eventually delete old deloyment directories


## Starting the index webservice

- `screen -S webservice-index`
- `. /opt/bashrc.sh`
- `cd /opt/embeddings`
- `./scripts/run-webservice-index-vm.sh`
- Test: [http://embeddings.cs.uni-paderborn.de:8008/ping](http://embeddings.cs.uni-paderborn.de:8008/ping)


# VM config overview

- Elasticsearch API
    - [ES :9200 version](https://embeddings.cs.upb.de:9200/)
    - [ES :9200 indexes](https://embeddings.cs.upb.de:9200/_cat/indices)
    - [ES :9200 mappings example](https://embeddings.cs.upb.de:9200/dbpedia_en_fr_15k_procrustes/_mapping)
- Elasticsearch 8.3.1
    - Manual start command: see Guide for [starting](https://www.elastic.co/guide/en/elasticsearch/reference/8.3/starting-elasticsearch.html), [stopping](https://www.elastic.co/guide/en/elasticsearch/reference/8.3/stopping-elasticsearch.html))
    - Check ES logs command: `tail /data/es8-logs/embcc.log`

# Archive

Use deployment commands in screen session.
Before, activate environment:

```bash
. /opt/anaconda3/etc/profile.d/conda.sh
conda activate embeddings

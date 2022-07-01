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


# VM config overview

- Elasticsearch API
    - [ES :9200 version](https://embeddings.cs.upb.de:9200/)
    - [ES :9200 indexes](https://embeddings.cs.upb.de:9200/_cat/indices)
- Elasticsearch 8.1.3
    - Documentation: [vm.md](https://github.com/dice-group/embeddings.cc/blob/master/docs/vm.md#elasticsearch-installation)
    - Configuration: /data/elasticsearch-8.1.3/config/elasticsearch.yml
        - path.data: /data/es8-data
        - path.logs: /data/es8-logs
    - Manual start command: `/data/elasticsearch-8.1.3/bin/elasticsearch -d -p /data/elasticsearch-8.1.3/pid/pid.txt`  
      (also see Guide for [starting](https://www.elastic.co/guide/en/elasticsearch/reference/8.1/starting-elasticsearch.html), [stopping](https://www.elastic.co/guide/en/elasticsearch/reference/8.1/stopping-elasticsearch.html))
- Elasticsearch 7.16.3 (until Apr 27, 2022)
    - Documentation: [vm.md - Apr 3, 2022](https://github.com/dice-group/embeddings.cc/blob/b0802888943a7ec93396d129a68f4fd605a66b55/docs/vm.md#elasticsearch-installation)
    - Configuration: /etc/elasticsearch/elasticsearch.yml
        - path.data: /data/elasticsearch
        - path.logs: /var/log/elasticsearch
- Check logs
    - `tail /data/es8-logs/embcc.log`


# Archive

Use deployment commands in screen session.
Before, activate environment:

```bash
. /opt/anaconda3/etc/profile.d/conda.sh
conda activate embeddings

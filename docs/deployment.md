# Deployment

- `kinit wilke` (or another upb user)
- `ssh wilke@embeddings.cs.upb.de`

## Outdated

- `kinit wilke`
- Copy code to /tmp:  
  `./scripts/vm-push.sh`
- `ssh wilke@embeddings.cs.upb.de`
- `. /opt/bashrc.sh`
- Move directory to /opt. **Do not overwrite** running code for one of the both webservices!  
  `sudo mv /tmp/embeddings.cc/ /opt/embeddings_cc_x`
- Unlink symlink
- Update symlink: `sudo ln -s /opt/embeddings_cc_e /opt/embeddings`
- `mkdir /opt/embeddings_cc_x/instance`
- `ln -s /opt/config.py /opt/embeddings_cc_x/instance/config.py`
- Restart inside screen by CTRL+C, `cd ../embeddings_cc_x`, :  
  `screen -r webservice-public`  
  `screen -r webservice-index`

## Initialize (e.g. after reboot)

Use deployment commands in screen session.
Before, activate environment:

```bash
. /opt/anaconda3/etc/profile.d/conda.sh
conda activate embeddings

# VM config overview

- /data/elasticsearch/ - outdated version 7.16.3 (see [config](https://github.com/dice-group/embeddings.cc/blob/b0802888943a7ec93396d129a68f4fd605a66b55/docs/vm.md#elasticsearch-installation))
- /data/elasticsearch-8.1.3/ - current ES
- /data/elasticsearch-8.1.3/config/elasticsearch.yml - current ES config file
- /data/es8-data/ - set in elasticsearch.yml
- /data/es8-logs/ - set in elasticsearch.yml
- /data/embeddings.cc-es8/ - current deployment
- /opt/anaconda3/
- /opt/cert/
- /opt/embeddings -> /data/embeddings.cc-es8/ **symlink to main version**
- /opt/embeddings_cc_e/ - outdated version 7.16.3
- /opt/config.py
- /opt/uwsgi.ini

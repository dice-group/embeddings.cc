# Deployment

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
```

## Local configuration

- Set up a local system similar to the [VM](vm.md).
- To start the components, use these commands:


### Start Elasticsearch

```bash
sudo systemctl start elasticsearch.service
```

### Start webservice (public)

```bash
conda activate embeddings
export FLASK_APP=webservice_public
export FLASK_RUN_PORT=1337
export FLASK_DEBUG=True
flask run
```

### Start webservice (index)

```bash
conda activate unikge
export FLASK_APP=webservice_index
export FLASK_RUN_PORT=8008
export FLASK_DEBUG=True
flask run
```
# Embeddings.cc Virtual Machine

- Hostname: `embeddings.cs.uni-paderborn.de`
- IP: `131.234.28.19`
- IPv6: `[::ffff:83ea:1c13]`
- Created: 2022-02-22
- OS: Debian GNU/Linux 11 (bullseye) (`cat /etc/*-release`)
- Ports open: 443/tcp, 8443/tcp 
- Hardware:
    - CPU: 4x Intel(R) Xeon(R) CPU E5-2695 v3 @ 2.30GHz (`cat /proc/cpuinfo`)
    - Memory: 32 GB (`free -h`)
    - Disk: 1007 GB (`/dev/sdb`, `df -h`)

## Logs

- Elasticsearch: `/data/es8-logs/`
- Elasticsearch garbage collection: `/data/elasticsearch-8.3.1/logs/gc.log`


## Elasticsearch installation

- Elasticsearch 7.16.3 documentation in [vm.md - Apr 3, 2022](https://github.com/dice-group/embeddings.cc/blob/b0802888943a7ec93396d129a68f4fd605a66b55/docs/vm.md#elasticsearch-installation)


### Elasticsearch 8.3.1

- [ES 8.3 installation](https://www.elastic.co/guide/en/elasticsearch/reference/8.3/targz.html#install-linux)
    - `cd /data`
    - `wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.3.1-linux-x86_64.tar.gz`
    - `wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.3.1-linux-x86_64.tar.gz.sha512`
    - `shasum -a 512 -c elasticsearch-8.3.1-linux-x86_64.tar.gz.sha512`
    - `tar -xzf elasticsearch-8.3.1-linux-x86_64.tar.gz`
    - `rm elasticsearch-8.3.1-linux-x86_64.tar.gz*`
https://www.elastic.co/guide/en/elasticsearch/reference/8.3/settings.html
- [ES 8.3 settings](https://www.elastic.co/guide/en/elasticsearch/reference/8.3/important-settings.html)
    - `cp /data/elasticsearch-8.3.1/config/elasticsearch.yml /data/elasticsearch-8.3.1/config/elasticsearch.original.yml`
    - `nano /data/elasticsearch-8.3.1/config/elasticsearch.yml`
    - cluster.name: embcc 
    - node.name: embcc-1
    - path.data: /data/es8-data
    - path.logs: /data/es8-logs
    - bootstrap.memory_lock: false
    - network.host: 0.0.0.0
    - http.port: 9200
- [ES 8.3 virtual memory](https://www.elastic.co/guide/en/elasticsearch/reference/8.3/vm-max-map-count.html)
    - `sudo sysctl -w vm.max_map_count=262144` (temp)
    - `sudo sysctl vm.max_map_count` (check)
    - `sudo nano /etc/sysctl.conf` (permanently)  
      `vm.max_map_count=262144`
- [ES 8.3 start](https://www.elastic.co/guide/en/elasticsearch/reference/8.3/starting-elasticsearch.html)
    - `/data/elasticsearch-8.3.1/bin/elasticsearch -d -p /data/elasticsearch-8.3.1/pid.txt`
- [ES 8.3 password](https://www.elastic.co/guide/en/elasticsearch/reference/8.3/reset-password.html)
    - `/data/elasticsearch-8.3.1/bin/elasticsearch-reset-password --username elastic --interactive`
- Autostart
    - `crontab -e`
    - `@reboot /data/elasticsearch-8.3.1/bin/elasticsearch -d -p /data/elasticsearch-8.3.1/pid.txt`
    - `sudo shutdown -r 0`


## Packages / software installation

- Anaconda (required for Faiss)
    - https://docs.conda.io/projects/conda/en/stable/user-guide/install/linux.html
    - `wget https://repo.anaconda.com/archive/Anaconda3-2022.10-Linux-x86_64.sh`
    - `bash Anaconda3-2022.10-Linux-x86_64.sh`
        - Installation path: `/upb/users/w/wilke/profiles/unix/cs/anaconda3`
        - Ended with Exception
        - `rm -rf anaconda3/`
    - `bash Anaconda3-2022.10-Linux-x86_64.sh`
        - Installation path: `/opt/anaconda`
        - Error: [Errno 28] No space left on device: '/opt/anaconda/pkgs/python-3.9.13-haa1d7c7_1'
        - `rm -rf /opt/anaconda3/`
    - `bash Anaconda3-2022.10-Linux-x86_64.sh`
        - Installation path: **`/data/anaconda`**
        - `conda --version` → **`conda 22.9.0`**
- Faiss
    - https://github.com/facebookresearch/faiss/
    - https://github.com/facebookresearch/faiss/blob/main/INSTALL.md
    - https://github.com/facebookresearch/faiss/wiki/Getting-started
    - (outdated:) `conda install -c pytorch faiss-cpu`
    - `conda activate embeddings`  
      `conda install -c conda-forge faiss-cpu` (**1.7.2**)


## Webservice installation

- Initial version, updates in [deployment.md](deployment.md)
- Copy code
    - `kinit wilke`
    - `./scripts/vm-push.sh`
    - `ssh wilke@embeddings.cs.upb.de`
    - `. /opt/bashrc.sh`
    - `sudo mv /tmp/embeddings.cc/ /opt/embeddings.cc/`
    - `mkdir /opt/embeddings.cc/instance`
    - `cp /opt/embeddings.cc/config.py /opt/`
    - `ln -s /opt/config.py /opt/embeddings.cc/instance/config.py`
- Anaconda environment
    - `conda create --name embeddings`
    - **`. /opt/anaconda3/etc/profile.d/conda.sh`**
    - `conda activate embeddings`
- Python modules
    - `cd /opt/embeddings.cc/`
    -  `conda install -c conda-forge --file requirements.txt`
        -  ImportError: cannot import name 'soft_unicode' from 'markupsafe'
    -  `pip install markupsafe==2.0.1`
- Webservice configuration
    - `python3 /opt/embeddings.cc/scripts/generate-salt-password.py XXX`
    - `cp /opt/embeddings.cc/config.py /opt/embeddings.cc/instance/config.py`
    - Inserted salt, hash and es-config
- Start webserver
    -  `export FLASK_APP=webservice_index`
    -  `export FLASK_RUN_PORT=8008`
    -  `flask run --host=0.0.0.0`
    - [http://embeddings.cs.uni-paderborn.de:8008/ping](http://embeddings.cs.uni-paderborn.de:8008/ping) --> Status: OK :)
  - New linux user 'embeddings'
    - `sudo useradd -m embeddings`
    - `sudo passwd embeddings`
    - `sudo -u embeddings -s` (also: how to switch to user)
  - sudo ln -s embeddings_cc_e embeddings

## Public webservice: Start configuration

### uWSGI

```ini
[uwsgi]
; This is the uWSGI config, located at /opt/uwsgi.ini
; How to start manually:
;  Log in as user 'embeddings'
;  Change directory to embeddings code root
;  Execute 'uwsgi /opt/uwsgi.ini'

home    = /opt/anaconda3
plugins = python3
mount   = /=webservice_public/wsgi.py

socket       = /tmp/embeddingscc.sock
chmod-socket = 666

master             = true
enable-threads     = true
manage-script-name = true
thunder-lock       = true
```

### systemd

- `sudo nano /etc/systemd/system/embeddings.service`
- `systemctl enable embeddings.service`
- `sudo systemctl start embeddings.service`
- `sudo shutdown -r 0`

```
# /etc/systemd/system/embeddings.service

[Unit]
Description=embeddings uwsgi
Requires=network.target
After=network.target

[Service]
WorkingDirectory=/opt/embeddings
User=embeddings
ExecStart=/usr/bin/uwsgi /opt/uwsgi.ini
TimeoutStopSec=30

[Install]
WantedBy=multi-user.target
```

## Misc

- Initialize bash (prompt and anaconda): **`. /opt/bashrc.sh`**
- [Kerberos Single-Sign-On](https://hilfe.uni-paderborn.de/Single-Sign-On_einrichten_unter_Linux): `kinit <imt-username>`
- Prompt (see [wiki.ubuntuusers.de](https://wiki.ubuntuusers.de/Bash/Prompt/)):  
  `PS1='\[\e]0;\u@\h: \w\a\]${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '`

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
- Note: Some ES8 commands in [Issue 39](https://github.com/dice-group/embeddings.cc/issues/39)
- Note: ES7 configuration in [previous version](https://github.com/dice-group/embeddings.cc/blob/82e7279f6506b58d4ad2538c91f924c6f33a27c4/docs/vm.md)


## Elasticsearch installation

### Elasticsearch 8

- Path: `/data/elasticsearch-8.1.3/config/elasticsearch.yml`
- [Elasticsearch Guide [8.1] » Set up Elasticsearch » Configuring Elasticsearch » Important Elasticsearch configuration](https://www.elastic.co/guide/en/elasticsearch/reference/8.1/important-settings.html)
    - cluster.name: embcc 
    - node.name: embcc-1
    - path.data: /data/es8-data
    - path.data: /data/es8-data
    - bootstrap.memory_lock: true
    - network.host: 0.0.0.0
    - http.port: 9208
- `sudo systemctl edit --force --full elasticsearch8.service` (force required to create file)
    - <strike>Command created file: `/etc/systemd/system/elasticsearch8.service`</strike>
    - <strike>State: Manual start works with bootstrap.memory_lock: false</strike>
- Added start by cron:
    - `crontab -e`
    - `@reboot /data/elasticsearch-8.1.3/bin/elasticsearch`
    - `sudo shutdown -r 0`
- `/data/elasticsearch-8.1.3/config/elasticsearch.yml`
    - `bootstrap.memory_lock: true`

## Packages installation

- Anaconda
    - Source: [https://docs.anaconda.com/anaconda/install/linux/](https://docs.anaconda.com/anaconda/install/linux/)
    - `wget https://repo.anaconda.com/archive/Anaconda3-2021.11-Linux-x86_64.sh`
    - `sudo bash Anaconda3-2021.11-Linux-x86_64.sh`
    - Directory: `/opt/anaconda3`
    - Output: `modified /root/.bashrc`


## Webservice installation

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

### Update symlink to use Elasticsearch 8

```
ls -l /opt/embeddings
lrwxrwxrwx 1 root root 15 Apr  3 12:47 /opt/embeddings -> embeddings_cc_e/
sudo systemctl stop embeddings.service  # takes 90 seconds, changed to 30
sudo unlink /opt/embeddings
sudo ln -s /data/embeddings.cc-es8/ /opt/embeddings
sudo systemctl start embeddings.service
```



## Misc

- Initialize bash (prompt and anaconda): **`. /opt/bashrc.sh`**
- [Kerberos Single-Sign-On](https://hilfe.uni-paderborn.de/Single-Sign-On_einrichten_unter_Linux): `kinit <imt-username>`
- Prompt (see [wiki.ubuntuusers.de](https://wiki.ubuntuusers.de/Bash/Prompt/)):  
  `PS1='\[\e]0;\u@\h: \w\a\]${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '`

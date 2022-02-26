# Embeddings.cc Virtual Machine

- Hostname: `embeddings.cs.uni-paderborn.de`
- IP: `131.234.28.19`
- Created: 2022-02-22
- OS: Debian GNU/Linux 11 (bullseye) (`cat /etc/*-release`)
- Ports open: 443/tcp, 8443/tcp 
- Hardware:
    - CPU: 4x Intel(R) Xeon(R) CPU E5-2695 v3 @ 2.30GHz (`cat /proc/cpuinfo`)
    - Memory: 32 GB (`free -h`)
    - Disk: 1007 GB (`/dev/sdb`, `df -h`)

## Elasticsearch installation

- Source: [https://www.elastic.co/guide/en/elasticsearch/reference/7.16/deb.html](https://www.elastic.co/guide/en/elasticsearch/reference/7.16/deb.html)
- Installation
    - `wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.16.3-amd64.deb`
    - `wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.16.3-amd64.deb.sha512`
    - `shasum -a 512 -c elasticsearch-7.16.3-amd64.deb.sha512`
    - `sudo dpkg -i elasticsearch-7.16.3-amd64.deb`
- Autostart
    - `sudo /bin/systemctl daemon-reload`
    - `sudo /bin/systemctl enable elasticsearch.service`
- Start
    - `sudo systemctl start elasticsearch.service`
    - `curl -X GET "127.0.0.1:9200/?pretty"` (Returns output after execution of previous command)
- Enable security
    - `sudo nano /etc/elasticsearch/elasticsearch.yml`
    - `# https://www.elastic.co/guide/en/elasticsearch/reference/7.16/security-minimal-setup.html`
    - `xpack.security.enabled: true`
    - `discovery.type: single-node`
    - `sudo systemctl restart elasticsearch.service`
- Set passwords
    - `sudo /usr/share/elasticsearch/bin/elasticsearch-setup-passwords interactive`
    - Inserted same password

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
    -  `pip3 install -r requirements.txt`
- Webservice configuration
    - `python3 /opt/embeddings.cc/scripts/generate-salt-password.py XXX`
    - `cp /opt/embeddings.cc/config.py /opt/embeddings.cc/instance/config.py`
    - Inserted salt, hash and es-config
- Start webserver
    -  `export FLASK_APP=webservice_index`
    -  `export FLASK_RUN_PORT=8008`
    -  `flask run --host=0.0.0.0`
    - [http://embeddings.cs.uni-paderborn.de:8008/ping](http://embeddings.cs.uni-paderborn.de:8008/ping) --> Status: OK :)

## Webservice start

- `screen -r webservice-index`
- `. /opt/bashrc.sh`
- `cd /opt/embeddings.cc/`
- `. /opt/anaconda3/etc/profile.d/conda.sh`
- `conda activate embeddings`
-  `export FLASK_APP=webservice_index`
-  `export FLASK_RUN_PORT=8008`
-  `flask run --host=0.0.0.0`

### Public webservice:

- `screen -r webservice`
- `. /opt/bashrc.sh`
- `cd /opt/embeddings.cc/`
- `. /opt/anaconda3/etc/profile.d/conda.sh`
- `conda activate embeddings`
-  `export FLASK_APP=webservice_public`
-  `export FLASK_RUN_PORT=8443`
-  `flask run --host=0.0.0.0`

## Misc

- Initialize bash (prompt and anaconda): **`. /opt/bashrc.sh`**
- [Kerberos Single-Sign-On](https://hilfe.uni-paderborn.de/Single-Sign-On_einrichten_unter_Linux): `kinit <imt-username>`
- Prompt (see [wiki.ubuntuusers.de](https://wiki.ubuntuusers.de/Bash/Prompt/)):  
  `PS1='\[\e]0;\u@\h: \w\a\]${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '`


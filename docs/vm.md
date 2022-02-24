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


## Misc

- [Kerberos Single-Sign-On](https://hilfe.uni-paderborn.de/Single-Sign-On_einrichten_unter_Linux)
    - `kinit <imt-username>`
- Prompt (see [wiki.ubuntuusers.de](https://wiki.ubuntuusers.de/Bash/Prompt/)):  
  `PS1='\[\e]0;\u@\h: \w\a\]${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '`
    - Put it in script, execute it using: `. ./opt/prompt.sh`
- Start flask (dev mode, in-build webserver)
    - `export FLASK_APP=webservice_index`
    - `export FLASK_RUN_PORT=8008`
    - `flask run`
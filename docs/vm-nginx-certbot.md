# Embeddings.cc Virtual Machine

## nginx / certbot / Let’s Encrypt

- `sudo nginx -s reload`
- `sudo nano /etc/nginx/sites-available/embeddings`
- `cat /var/log/nginx/error.log`
- `cat /var/log/nginx/access.log`

### nginx configuration

```
server {
    if ($host = embeddings.cc) {
        return 301 https://$host$request_uri;
    } # managed by Certbot

  server_name embeddings.cc embeddings.cs.uni-paderborn.de;
  listen 80 default_server;
  listen [::]:80 default_server;
  location / { try_files $uri @embeddings; }
  location @embeddings {
    include uwsgi_params;
    uwsgi_pass unix:/tmp/embeddingscc.sock;
  }
}

server {
  server_name embeddings.cc embeddings.cs.uni-paderborn.de;
  listen 8443 ssl default_server;
  listen [::]:8443 ssl default_server;
  ssl_certificate /opt/cert/embeddings.cs.uni-paderborn.de.pem;
  ssl_certificate_key /opt/cert/embeddings.cs.uni-paderborn.de.key;
  location / { try_files $uri @embeddings; }
  location @embeddings {
    include uwsgi_params;
    uwsgi_pass unix:/tmp/embeddingscc.sock;
  }
  # Redirect, if HTTP protocol used
  error_page 497 https://$host:$server_port$request_uri;
}

server {
  server_name embeddings.cc embeddings.cs.uni-paderborn.de;
  listen 443 ssl default_server;
  listen [::]:443 ssl default_server;
    ssl_certificate /etc/letsencrypt/live/embeddings.cc/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/embeddings.cc/privkey.pem; # managed by Certbot
  location / { try_files $uri @embeddings; }
  location @embeddings {
    include uwsgi_params;
    uwsgi_pass unix:/tmp/embeddingscc.sock;
  }
  # Redirect, if HTTP protocol used
  error_page 497 https://$host:$server_port$request_uri;
}
```

### certbot installation

- https://certbot.eff.org/instructions?ws=nginx&os=debianbuster
- `sudo apt install snapd`
- `sudo snap install core; sudo snap refresh core`
- `sudo snap install --classic certbot`
- `sudo ln -s /snap/bin/certbot /usr/bin/certbot`

```
sudo certbot --nginx -d embeddings.cc
Saving debug log to /var/log/letsencrypt/letsencrypt.log
Requesting a certificate for embeddings.cc

Successfully received certificate.
Certificate is saved at: /etc/letsencrypt/live/embeddings.cc/fullchain.pem
Key is saved at:         /etc/letsencrypt/live/embeddings.cc/privkey.pem
This certificate expires on 2022-05-31.
These files will be updated when the certificate renews.
Certbot has set up a scheduled task to automatically renew this certificate in the background.

Deploying certificate
Could not install certificate

NEXT STEPS:
- The certificate was saved, but could not be installed (installer: nginx). After fixing the error shown below, try installing it again by running:
  certbot install --cert-name embeddings.cc

Could not automatically find a matching server block for embeddings.cc. Set the `server_name` directive to use the Nginx installer.
Ask for help or search for solutions at https://community.letsencrypt.org. See the logfile /var/log/letsencrypt/letsencrypt.log or re-run Certbot with -v for more details.
```

```
sudo certbot install --cert-name embeddings.cc
Saving debug log to /var/log/letsencrypt/letsencrypt.log
Deploying certificate
Successfully deployed certificate for embeddings.cc to /etc/nginx/sites-enabled/embeddings
```

```
sudo certbot renew --dry-run
Saving debug log to /var/log/letsencrypt/letsencrypt.log

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Processing /etc/letsencrypt/renewal/embeddings.cc.conf
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Simulating renewal of an existing certificate for embeddings.cc

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Congratulations, all simulated renewals succeeded: 
  /etc/letsencrypt/live/embeddings.cc/fullchain.pem (success)
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
```

```
systemctl list-timers
NEXT                        LEFT          LAST                        PASSED       UNIT                         ACTIVATES
Wed 2022-03-02 13:38:43 CET 4min 46s left Wed 2022-03-02 13:28:39 CET 5min ago     apply-ipxe-policy.timer      apply-ipxe-policy.service
Wed 2022-03-02 13:39:00 CET 5min left     Wed 2022-03-02 13:09:01 CET 24min ago    phpsessionclean.timer        phpsessionclean.service
Wed 2022-03-02 13:57:55 CET 23min left    Wed 2022-03-02 12:08:26 CET 1h 25min ago apt-daily.timer              apt-daily.service
Wed 2022-03-02 14:34:05 CET 1h 0min left  Wed 2022-03-02 13:31:41 CET 2min 15s ago apt-daily-upgrade.timer      apt-daily-upgrade.service
Wed 2022-03-02 16:13:56 CET 2h 39min left Tue 2022-03-01 16:13:56 CET 21h ago      systemd-tmpfiles-clean.timer systemd-tmpfiles-clean.service
Wed 2022-03-02 19:20:00 CET 5h 46min left n/a                         n/a          snap.certbot.renew.timer     snap.certbot.renew.service
Thu 2022-03-03 00:00:00 CET 10h left      Wed 2022-03-02 00:00:02 CET 13h ago      logrotate.timer              logrotate.service
Thu 2022-03-03 00:00:00 CET 10h left      Wed 2022-03-02 00:00:02 CET 13h ago      man-db.timer                 man-db.service
Thu 2022-03-03 01:31:08 CET 11h left      Wed 2022-03-02 00:30:05 CET 13h ago      clean-var-log.timer          clean-var-log.service
Sun 2022-03-06 03:10:26 CET 3 days left   Sun 2022-02-27 03:10:52 CET 3 days ago   e2scrub_all.timer            e2scrub_all.service
Mon 2022-03-07 00:21:22 CET 4 days left   Mon 2022-02-28 00:19:24 CET 2 days ago   fstrim.timer                 fstrim.service
```

### nginx configuration before certbot

- `sudo cp -r /etc/ssl/private/ /opt/cert/`
- https://wiki.ubuntuusers.de/nginx/
- `sudo apt-get install nginx`
- `sudo unlink /etc/nginx/sites-enabled/default`
- `sudo nano /etc/nginx/sites-available/embeddings`

```
server {
  server_name embeddings.cc embeddings.cs.uni-paderborn.de
  listen 80 default_server;
  listen [::]:80 default_server;
  location / { try_files $uri @embeddings; }
  location @embeddings {
    include uwsgi_params;
    uwsgi_pass unix:/tmp/embeddingscc.sock;
  }
}

server {
  server_name embeddings.cc embeddings.cs.uni-paderborn.de;
  listen 8443 ssl default_server;
  listen [::]:8443 ssl default_server;
  ssl_certificate /opt/cert/embeddings.cs.uni-paderborn.de.pem;
  ssl_certificate_key /opt/cert/embeddings.cs.uni-paderborn.de.key;
  location / { try_files $uri @embeddings; }
  location @embeddings {
    include uwsgi_params;
    uwsgi_pass unix:/tmp/embeddingscc.sock;
  }
  # Redirect, if HTTP protocol used
  error_page 497 https://$host:$server_port$request_uri;
}
```

- `sudo ln -s /etc/nginx/sites-available/embeddings /etc/nginx/sites-enabled/`
- `sudo nginx -s reload`
#! /bin/bash
apt-get update
apt install curl nginx letsencrypt certbot python3-certbot-nginx -y
apt-get install python3 python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools -y
apt-get install python3-venv -y

mkdir /root/project

cat <<EOT> /root/project/wsgi.py
from flaskapp import app

if __name__ == "__main__":
    app.run()
EOT

cat <<EOT> /etc/systemd/system/flask.service
[Unit]
Description=Gunicorn instance to serve Flask
After=network.target
[Service]
User=root
Group=www-data
WorkingDirectory=/root/project
Environment="PATH=/root/project/venv/bin"
ExecStart=/root/project/venv/bin/gunicorn --bind 0.0.0.0:5000 wsgi:app
[Install]
WantedBy=multi-user.target
EOT

chown -R root:www-data /root/project
chmod -R 775 /root/project

systemctl daemon-reload

systemctl start flask
systemctl enable flask

sudo ufw allow 'Nginx HTTP'
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'

cd /root/project/
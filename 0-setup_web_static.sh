#!/usr/bin/env bash
# A Bash script that sets up my web servers for the deployment of web_static

# install nginx if it isn't install

if ! command -v nginx > /dev/null 2>&1; then
    apt-get -y update
    apt-get -y install nginx
fi

# Check if directories exist
dir="/data/web_static/shared/"
dir2="/data/web_static/releases/"
dir3="/data/web_static/releases/test/"
html_file="/data/web_static/releases/test/index.html"
link="/data/web_static/current"
if [ ! -d "$dir" ]; then
    mkdir -p "$dir"
fi

if [ ! -d "$dir2" ]; then
    mkdir -p "$dir2"
fi

if [ ! -d "$dir3" ]; then
    mkdir -p "$dir3"
fi

if [ ! -f "$html_file" ]; then
    cat << _EOF_ > "$html_file"
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>
_EOF_
fi

# Check if the symbolic link exists

if [ -L "$link" ]; then
    rm "$link"
fi
ln -s "$dir3" "$link"
chown -R ubuntu /data/
chgrp -R ubuntu /data/

echo "Hello World!" > /var/www/html/index.html
SERVER_confg=\
"server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name _;

    location / {
        root /var/www/html;
        index index.html;
        add_header X-Served-By $HOSTNAME;
    }
    location /hbnb_static {
        alias /data/web_static/current/;
        index index.html;
        add_header X-Served-By $HOSTNAME;
    }
}"
echo -e "$SERVER_confg" > /etc/nginx/sites-available/default
service nginx restart



#!/usr/bin/env bash
# Write a Bash script that sets up your web servers for the deployment of web_static.

# Check if nginx web server has not been installed and install it
if ! command -v nginx &> /dev/null; then
	apt-get -y update && apt-get -y install nginx
fi

# Create individual directory in the directories variable if it not already exists
directories=("/data/" "/data/web_static/" "/data/web_static/releases/" "/data/web_static/shared/" "/data/web_static/releases/test/")
for directory in "${directories[@]}"; do
    if [ ! -d "$directory" ]; then
	    mkdir -p "$directory"
    fi
done

# Add the content to be served
cat <<EOF > /data/web_static/releases/test/index.html
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>
EOF

# Check if symbolic link already exists and delete it
if [ -L "/data/web_static/current" ]; then
    rm -f "/data/web_static/current"
fi

# Create a symbolic link
ln -s "/data/web_static/releases/test/" "/data/web_static/current"

# Give the user and group ownership of /data/ to ubuntu recursively
chown -R ubuntu:ubuntu /data/

mkdir -p /var/www/html
chmod 755 /var/www/html
echo "Holberton School" > /var/www/html/index.html

the_hostname=$(hostname)
# Configure the server block
cat <<EOF > /etc/nginx/sites-available/default
server {
        listen 80;
        listen [::]:80;

        root /var/www/html;
        index index.html index.htm;

        server_name agroelectronics.tech;
	add_header X-Served-By $the_hostname;

	location /hbnb_static {
		#location of the the html content to serve
		alias /data/web_static/current/;
	}
}
EOF
service nginx restart

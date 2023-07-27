#!/usr/bin/env bash
# set up the web server for the deployment of web_static

apt update -y
which nginx > testfile.txt
file="testfile.txt"

if [ ! -s "$file" ]
then
	apt install nginx -y
fi
rm $file

mkdir -p /data/web_static/releases/test
mkdir -p /data/web_static/shared
echo -e "<html>\n  <head>\n  </head>\n  <body>\n    Holberton School\n  </body>\n</html>" > /data/web_static/releases/test/index.html
ln -sf /data/web_static/releases/test/ /data/web_static/current
chown -R ubuntu:ubuntu /data
line="\\\tlocation /hbnb_static {\n\t\talias /data/web_static/current;\n\t}"
sed -i "60i $line" /etc/nginx/sites_enabled/default
service nginx restart

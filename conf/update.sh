#!/bin/sh

cd ../ShortURL/

git pull

pip install -r requirements.txt

cd ../shorturl-conf/


chown www-data:www-data /home/www -R



./stop.sh
./start.sh

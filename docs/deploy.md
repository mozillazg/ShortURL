# Deployment

## clone code

    cd /home/www/
    git clone https://github.com/mozillazg/ShortURL.git

## install dependencies

    pip install gunicorn
    pip install -r requirements.txt

## database

use shorturl/db.sql

## configure

    mkdir /home/www/shorturl-conf/
    cp -r conf/* /home/www/shorturl-conf/

### nginx

add `include /home/www/*-conf/nginx.conf;` to `http {...}` (`/etc/nginx/nginx.conf`)

change **server_name** (`/home/www/shorturl-conf/nginx.conf`)

    nginx -s reload

## run

    cd /home/www/shorturl-conf/
    chmod +x *.sh
* start
  `./start.sh`
* stop
  `./stop.sh`
* restart
  `./restart.sh`
* update code
  `./update.sh`

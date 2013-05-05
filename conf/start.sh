#!/bin/sh

gunicorn_conf="`pwd`/gunicorn.py"

cd /home/www/ShortURL/

gunicorn deploy:app_wsgi -c $gunicorn_conf -D

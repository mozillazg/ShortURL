workers = 2
bind = 'unix:/tmp/shorturl.sock'
proc_name = 'shorturl'
pidfile = '/tmp/shorturl.pid'
user = 'www-data'
group = 'www-data'
errorlog = '/home/www/shorturl-conf/gunicorn_error.log'

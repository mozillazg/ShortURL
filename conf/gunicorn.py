workers = 2
bind = 'unix:/var/run/shorturl.sock'
proc_name = 'shorturl'
pidfile = '/var/run/shorturl.pid'
user = 'www-data'
group = 'www-data'
errorlog = '/home/www/shorturl-conf/gunicorn_error.log'

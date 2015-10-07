# shorturl

A URL shortener site powered by Django.

## Features

* Shorten URL.
* QR Code.

## Demo

<http://3sd.me>

## 开发

1. `cp shorturl/shorturl/settings.py.sample shorturl/shorturl/settings.py`
2. 修改数据库信息: `vim shorturl/shorturl/settings.py`
3. `python manage.py migrate`
4. 运行服务: `python manage.py runserver`

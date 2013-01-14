# shorturl

A URL shortener site powered by Python and web.py.

## Features

* Shorten URL.
* QR Code.
* Support all most URL scheme.

## Demo

<http://3sd.me>

## API

Long -> Short

    URL: http://3sd.me/j/shorten
    Method: POST
    Parameters: url
    Return: JSON

Examples:

    $ curl 3sd.me/j/shorten -d "url=baidu.com"
    {"shorten": "http://3sd.me/Jh8x3", "expand": "http://baidu.com"}

Short -> Long

    URL: http://3sd.me/j/expand
    Method: POST
    Parameters: shorten
    Return: JSON

Examples:

    $ curl 3sd.me/j/expand -d "shorten=Jh8x3"
    {"shorten": "http://3sd.me/Jh8x3", "expand": "http://baidu.com"}

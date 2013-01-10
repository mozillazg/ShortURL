# shorturl

A URL shortener site powered by Python 2.6 and web.py 2.

## Features

* Shorten URL.
* QR Code.
* Support all most URL scheme.

## Demo

<http://3sd.me>

### API

#### Long -> Short

    URL: http://3sd.me/js/shorten
    Method: POST
    Parameters: url
    Return: JSON

Sample:

curl:

    $ curl 3sd.me/j/shorten -d "url=baidu.com"
    {"shorten": "http://3sd.me/Jh8x3", "expand": "http://baidu.com"}

[httpie](https://github.com/jkbr/httpie):

    $ http --form POST 3sd.me/j/shorten url=baidu.com
    HTTP/1.1 200 OK
    Cache-Control: no-cache
    Connection: keep-alive
    Content-Type: application/json
    Date: Thu, 10 Jan 2013 15:30:39 GMT
    Expires: Thu, 10 Jan 2013 15:22:22 GMT
    Keep-Alive: timeout=20
    Server: nginx/1.2.1
    Transfer-Encoding: chunked

    {
        "expand": "http://baidu.com",
        "shorten": "http://3sd.me/Jh8x3"
    }


#### Short -> Long

    URL: http://3sd.me/js/expand
    Method: POST
    Parameters: shorten
    Return: JSON

Sample:

curl:

    $ curl 3sd.me/j/expand -d "shorten=Jh8x3"
    {"shorten": "http://3sd.me/Jh8x3", "expand": "http://baidu.com"}

httpie:

    $ http --form POST 3sd.me/j/expand shorten=Jh8x3
    HTTP/1.1 200 OK
    Cache-Control: no-cache
    Connection: keep-alive
    Content-Type: application/json
    Date: Thu, 10 Jan 2013 15:31:27 GMT
    Expires: Thu, 10 Jan 2013 15:23:11 GMT
    Keep-Alive: timeout=20
    Server: nginx/1.2.1
    Transfer-Encoding: chunked

    {
        "expand": "http://baidu.com",
        "shorten": "http://3sd.me/Jh8x3"
    }

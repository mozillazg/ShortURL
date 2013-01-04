# shorturl

A URL shortener site powered by Python 2.6 and web.py 2.

## Features

* Shorten URL.
* QR Code.
* Support all most URL scheme.

## Demo

<http://3sd.me>

### 截图

![]( )

![]( )

### API

#### Long -> Short

    URL: http://3sd.me/js/shorten
    Method: POST
    Parameters: url
    Return: JSON

Sample:

        

#### Short -> Long

    URL: http://3sd.me/js/expand
    Method: POST
    Parameters: shorten
    Return: JSON

Sample:

        


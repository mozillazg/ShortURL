#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urlparse
import urllib
import json
import re
import web
import settings
import models

web.config.debug = settings.DE_BUG
render = web.template.render(settings.TEMPLATE_DIR,
                             base=settings.BASE_TEMPLATE)
app = web.application(settings.URLS, globals())
DB_R = settings.DATABASES_READ
DB_W = settings.DATABASES_WRITE
db = models.DB(db_read_kwargs=DB_R, db_write_kwargs=DB_W)


class Index(object):
    def GET(self):
        return render.index()
        #return web.input()


class Shorten(object):
    def __init__(self):
        self.db = db

    def add_scheme(self, url):
        # 支持的 URL 协议
        protocols = ['http://', 'https://', 'ftp://',
                     'irc://', 'git://', 'git@', 'ssh://', 'svn://',
                     'mailto:', 'tencent://',
                     'ed2k://', 'magnet:?', 'thunder://', 'flashget://',
                     'qqdl://', 'bc://', 'fs2you://',
                     'zhushou360://', 'itunes://', 'macappstore://',
                     # 'javascript:', 'aliim://', 'yy://', 'bc://', 'bctp://',
                     ]
        for i in protocols:
            if long_url.lower.startswith(i):
                break
        else:
            long_url = 'http://' + long_url
        return long_url

    def POST(self, get_json=False):
        long_url = web.input(url='').url.encode('utf8').strip()
        if not long_url:
            return web.badrequest()

        # long_url = add_scheme(long_url)
        url_split = urlparse.urlsplit(long_url)
        url_scheme = url_split.scheme
        url_unquote = ''.join(url_split[1:])
        long_url = url_scheme + '://' + urllib.quote(url_unquote)
        print repr(long_url)

        exists = self.db.exist_expand(long_url)
        if exists:
            shorten = exists.shorten
        else:
            shorten = self.db.add_url(long_url).shorten
        shorten = web.ctx.homedomain + '/' + shorten
        if get_json:
            web.header('Content-Type', 'application/json')
            return json.dumps({'shorten': shorten, 'expand': long_url})
        else:
            qr_api = 'http://qrcode101.duapp.com/qr?chl=%s&chs=200x200&chld=M|0'
            shortens = web.storage({
                'url': shorten,
                'qr': qr_api % urllib.quote(shorten),
                })
            return render.shorten(shortens)


class Expand(object):
    def __init__(self):
        self.db = db

    def get_expand(self, shorten):
        result = self.db.get_expand(shorten)
        if result:
            return result.expand

    def GET(self, shorten):
        if not shorten:
            return web.seeother('/')
        expand = self.get_expand(shorten)
        if expand:
            return web.redirect(expand)
        else:
            return web.notfound()

    def POST(self):
        shorten = web.input(shorten='').shorten.encode('utf8').strip()
        web.header('Content-Type', 'application/json')
        if shorten and re.match('[a-zA-Z0-9]{5,}$', str(shorten)):
            expand = self.get_expand(shorten)
            if expand:
                return json.dumps({'shorten': shorten, 'expand': expand})
            else:
                return json.dumps({'shorten': '', 'expand': ''})
        else:
            return json.dumps({'shorten': '', 'expand': ''})


if __name__ == '__main__':
    app.run()

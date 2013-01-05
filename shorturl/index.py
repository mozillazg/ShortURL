#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import re
import web
from libs.qrcode import QRCode, ErrorCorrectLevel
import settings
import models

debug = web.config.debug = settings.DE_BUG
render = web.template.render(settings.TEMPLATE_DIR,
                             base=settings.BASE_TEMPLATE)
app = web.application(settings.URLS, globals())
db = models.DB(settings.DATABASES)


class Index(object):
    def GET(self):
        return render.index()


class Shorten(object):
    def __init__(self):
        self.db = db

    def add_scheme(self, url):
        """add_scheme(url) -> url

        给 URL 添加 scheme(qq.com -> http://qq.com)
        """
        # 支持的 URL scheme
        scheme2 = re.compile(r'(?i)^[a-z][a-z0-9+.\-]*://')
        scheme3 = ('git@', 'mailto:', 'javascript:', 'about:', 'opera:',
                   'afp:', 'aim:', 'apt:', 'attachment:', 'bitcoin:',
                   'callto:', 'cid:', 'data:', 'dav:', 'dns:', 'fax:', 'feed:',
                   'gg:', 'go:', 'gtalk:', 'h323:', 'iax:', 'im:', 'itms:',
                   'jar:', 'magnet:', 'maps:', 'message:', 'mid:', 'msnim:',
                   'mvn:', 'news:', 'palm:', 'paparazzi:', 'platform:',
                   'pres:', 'proxy:', 'psyc:', 'query:', 'session:', 'sip:',
                   'sips:', 'skype:', 'sms:', 'spotify:', 'steam:', 'tel:',
                   'things:', 'urn:', 'uuid:', 'view-source:', 'ws:', 'xfire:',
                   'xmpp:', 'ymsgr:', 'doi:',
                   )
        url_lower = url.lower()

        scheme = scheme2.match(url_lower)
        if not scheme:
            for scheme in scheme3:
                url_splits = url_lower.split(scheme)
                if len(url_splits) > 1:
                    break
            else:
                url = 'http://' + url
        return url

    def qrcode_table(self, data, type_number=4, error_correct_level='H'):
        """qrcode_table(data) -> html

        生成 QR Code html 表格，可以通过 css 控制黑白块的显示
        """
        if error_correct_level == 'L':
            error_correct_level = ErrorCorrectLevel.L
        elif error_correct_level == 'M':
            error_correct_level = ErrorCorrectLevel.M
        elif error_correct_level == 'Q':
            error_correct_level = ErrorCorrectLevel.Q
        else:
            error_correct_level = ErrorCorrectLevel.H

        qr = QRCode()
        qr.setTypeNumber(type_number)
        qr.setErrorCorrectLevel(error_correct_level)
        qr.addData(data)
        qr.make()

        html = '<table id="qrcode-table">'
        for r in range(qr.getModuleCount()):
            html += "<tr>"
            for c in range(qr.getModuleCount()):
                if qr.isDark(r, c):
                    html += '<td class="dark" />'
                else:
                    html += '<td class="white" />'
            html += '</tr>'
        html += '</table>'
        return html

    def POST(self, get_json=False):
        url = web.input(url='').url.encode('utf8').strip()
        if not url:
            return web.badrequest()

        url = self.add_scheme(url)
        if debug:
            print repr(url)

        exists = self.db.exist_expand(url)
        if exists:
            shorten = exists.shorten
        else:
            shorten = self.db.add_url(url).shorten
        shorten = web.ctx.homedomain + '/' + shorten

        if get_json:
            web.header('Content-Type', 'application/json')
            return json.dumps({'shorten': shorten, 'expand': url})
        else:
            shortens = web.storage({'url': shorten,
                                    'qr_table': self.qrcode_table(shorten),
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
        print repr(expand)
        if expand:
            return web.redirect(expand)
        else:
            return web.index()

    def POST(self):
        shorten = web.input(shorten='').shorten.encode('utf8').strip()
        web.header('Content-Type', 'application/json')
        if shorten and re.match('[a-zA-Z0-9]{5,}$', str(shorten)):
            expand = self.get_expand(shorten)
            if debug:
                print repr(expand)
            if expand:
                shorten = web.ctx.homedomain + '/' + shorten
                return json.dumps({'shorten': shorten, 'expand': expand})
            else:
                return json.dumps({'shorten': '', 'expand': ''})
        else:
            return json.dumps({'shorten': '', 'expand': ''})


if __name__ == '__main__':
    # web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
    app.run()

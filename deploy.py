#!/usr/bin/env python
# -*- coding: utf-8 -*-

from shorturl.index import app

app_wsgi = app.wsgifunc()

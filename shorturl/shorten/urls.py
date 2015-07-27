#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.conf.urls import patterns, url

from .views import ShortenView, ExpandView, QrcodeView

urlpatterns = patterns(
    '',
    url(r'^$', ShortenView.as_view(), name='shorten'),
    url(r'^qr/$', QrcodeView.as_view(), name='qrcode'),
    url(r'^(?P<code>\w{5,15})/$', ExpandView.as_view(), name='url'),
)

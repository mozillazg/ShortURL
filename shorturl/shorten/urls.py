#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.conf import settings
from django.conf.urls import patterns, url

from .views import ShortenView, ExpandView, QrcodeView

MIN_LENGTH = settings.SHORTEN_CODE_MIN_LENGTH


urlpatterns = patterns(
    '',
    url(r'^$', ShortenView.as_view(), name='shorten'),
    url(r'^qr/$', QrcodeView.as_view(), name='qrcode'),
    url(r'^(?P<code>\w{%s,15})/$' % MIN_LENGTH,
        ExpandView.as_view(), name='url'),
)

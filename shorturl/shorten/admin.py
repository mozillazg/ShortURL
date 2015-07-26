#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.contrib import admin
from django.utils.html import format_html

from .models import ShortenURL


@admin.register(ShortenURL)
class ShortenURLAdmin(admin.ModelAdmin):
    def format_url(self, url, title=None):
        return format_html('<a href="{url}" target="_blank">{title}</a>',
                           url=url, title=title or url)

    def _url(self, obj):
        return self.format_url(obj.url)
    _url.short_description = '短地址'

    def _long_url(self, obj):
        return self.format_url(obj.long_url)
    _long_url.short_description = '长地址'

    def qrcode(self, obj):
        return self.format_url(obj.qrcode, title='查看二维码')
    qrcode.short_description = '二维码'

    exclude = ('code', 'created_at', 'updated_at')
    list_display = ('id', '_url', 'qrcode', '_long_url', 'note',
                    'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('code', 'long_url', 'note')
    list_per_page = 30

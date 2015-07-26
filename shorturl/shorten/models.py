#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import urllib

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now

from .libs.short_url import encode_url

MIN_LENGTH = settings.SHORTEN_CODE_MIN_LENGTH


@python_2_unicode_compatible
class ShortenURL(models.Model):
    code = models.CharField('短地址 hash', max_length=15, db_index=True)
    long_url = models.TextField('长地址', db_index=True)
    note = models.TextField('备注', default='', blank=True)

    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)

    class Meta:
        db_table = 'url'  # 兼容旧数据库
        verbose_name = '短网址'
        verbose_name_plural = '短网址管理'

    def __str__(self):
        return '<ShortenURL: %s>' % self.code

    def save(self, *args, **kwargs):
        self.long_url = self.long_url.strip()
        self.updated_at = now()
        if self.pk and not self.code:
            self.code = self.new_code(self.pk)
        super(ShortenURL, self).save(*args, **kwargs)
        if not self.code:
            self.save()

    def get_absolute_url(self):
        uri = reverse('shorten_url:url', kwargs={'code': self.code})
        return settings.SITE_URL + uri

    @property
    def url(self):
        return self.get_absolute_url()

    @property
    def qrcode(self):
        uri = reverse('shorten_url:qrcode')
        params = urllib.urlencode({'content': self.url})
        return settings.SITE_URL + uri + '?' + params

    @classmethod
    def shorten(cls, long_url):
        long_url = long_url.strip()
        instance, _ = cls.objects.get_or_create(long_url=long_url)
        instance.save()
        return instance

    @classmethod
    def expand(cls, code):
        code = code.strip()
        return cls.objects.filter(code=code).first()

    @staticmethod
    def new_code(n):
        return encode_url(n, min_length=MIN_LENGTH)

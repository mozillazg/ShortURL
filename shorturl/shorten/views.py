#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import logging
import json

from django.conf import settings
from django.http import (
    HttpResponse, Http404, HttpResponsePermanentRedirect,
    HttpResponseRedirect, JsonResponse
)
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import View

from .models import ShortenURL
from .utils import gen_qrcode, img2base64, qr2data

logger = logging.getLogger(__name__)


class ShortenView(View):
    """网址缩短"""
    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super(ShortenView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render_to_response(
            'shorten/index.html', context_instance=RequestContext(request)
        )

    def post(self, request, *args, **kwargs):
        long_url = ''
        if request.is_ajax():
            try:
                data = json.loads(request.read())
                long_url = data.get('long_url', '')
                require_qrcode = data.get('qrcode', False)
            except Exception as e:
                logger.exception(e)
        else:
            long_url = request.POST.get('long_url')
            require_qrcode = request.POST.get('qrcode', 'false') == 'true'

        if not long_url:
            data = {
                'message': 'long_url 不能为空'
            }
            return JsonResponse(data=data, status=400)

        instance = ShortenURL.shorten(long_url)
        if require_qrcode:
            qr = gen_qrcode(instance.url)
            data = qr2data(qr)
            content_typ = 'image/png'
            img = img2base64(qr2data(qr), mime_type=content_typ)
        else:
            img = ''

        data = {
            'hash': instance.code,
            'long_url': instance.long_url,
            'url': instance.url,
            'qrcode': img,
        }
        return JsonResponse(data=data)


class ExpandView(View):
    """获取长网址"""
    def get(self, request, code, *args, **kwargs):
        """重定向到源地址"""
        instance = ShortenURL.expand(code)
        if instance is None:
            raise Http404()
        else:
            if settings.REDIRECT_STATUS == 301:
                return HttpResponsePermanentRedirect(instance.long_url)
            else:
                return HttpResponseRedirect(instance.long_url)


class QrcodeView(View):
    """二维码"""
    def get(self, request, *args, **kwargs):
        # 包含的文本信息
        content = request.GET.get('content', '')
        # 图片大小 120 x 120
        size = request.GET.get('size', '120')
        if not size.isdigit():
            size = 120
        size = int(size)
        # 纠错级别
        level = request.GET.get('level', 'M')
        if level.upper() not in ['L', 'M', 'Q', 'H']:
            level = 'M'
        # 二维码离图片边框的距离
        border = request.GET.get('border', '4')
        if not border.isdigit():
            border = 4
        border = int(border)

        qr = gen_qrcode(content, level=level, border=border)
        data = qr2data(qr)
        content_typ = 'image/png'
        return HttpResponse(data, content_type=content_typ)

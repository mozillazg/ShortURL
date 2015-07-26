#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from base64 import b64encode
import cStringIO

import qrcode


def gen_qrcode(content, version=1, level='L', box_size=10, border=0):
    qr = qrcode.QRCode(
        version=version,
        error_correction=getattr(qrcode.constants, 'ERROR_CORRECT_' + level),
        box_size=box_size,
        border=border,
    )
    qr.add_data(content)
    qr.make(fit=True)
    img = qr.make_image()
    return img


def qr2data(qr, type='png'):
    io = cStringIO.StringIO()
    qr.save(io, type)
    data = io.getvalue()
    io.close()
    return data


def img2base64(data, mime_type='image/png'):
    return 'data:{0};base64,{1}'.format(mime_type, b64encode(data))

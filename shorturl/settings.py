#!/usr/bin/env python
# -*- coding: utf-8 -*-

IS_LOCAL = True if True else False
DE_BUG = True
TEMPLATE_DIR = 'templates/'
BASE_TEMPLATE = 'base'

URLS = (
    '/', 'Index',
    '(/j)?/shorten', 'Shorten',
    '/([0-9a-zA-Z]{5,})', 'Expand',
    '/j/expand', 'Expand',
)

if IS_LOCAL:
    DATABASES_READ = {
        'dbn': 'mysql',
        'db': 'shorturl',
        'user': 'readonly',
        'pw': 'readonly',
        'host': 'localhost',
        'port': 3306,
    }
    DATABASES_WRITE = {
        'dbn': 'mysql',
        'db': 'shorturl',
        'user': 'py',
        'pw': 'py',
        'host': 'localhost',
        'port': 3306,
    }
else:
    DATABASES_READ = {
        'dbn': 'mysql',
        'db': '',
        'user': '',
        'pw': '',
        'host': '',
        'port': 3306,
    }
    DATABASES_WRITE = {
        'dbn': 'mysql',
        'db': '',
        'user': '',
        'pw': '',
        'host': '',
        'port': 3306,
    }

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web
from libs import short_url


class DB(object):
    def __init__(self, db_kwargs):
        self.db = web.database(**db_kwargs)

    def exist_expand(self, long_url):
        """检查数据库中是否已有相关记录，有则返回短 URL
        """
        result = self.db.where(table='url', what='shorten',
                               expand=long_url)
        if result:
            return result[0]

    def add_url(self, long_url):
        """添加 URL，返回短 URL
        """
        id_ = self.db.insert(tablename='url', seqname='id', shorten='',
                             expand=long_url)
        shorten = short_url.encode_url(id_)
        self.db.update(tables='url', shorten=shorten,
                       where='id=$id_', vars=locals())
        return web.storage(shorten=shorten)

    def get_expand(self, shorten):
        """根据短 URL 返回原始 URL
        """
        result = self.db.where(table='url', what='expand',
                               shorten=shorten)
        if result:
            return result[0]

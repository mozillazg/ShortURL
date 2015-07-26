# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shorten', '0003_auto_20150725_2203'),
    ]

    operations = [
        migrations.AddField(
            model_name='shortenurl',
            name='note',
            field=models.TextField(default='', verbose_name='\u5907\u6ce8', blank=True),
        ),
    ]

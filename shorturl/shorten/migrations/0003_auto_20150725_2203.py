# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shorten', '0002_auto_20150725_2158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shortenurl',
            name='long_url',
            field=models.TextField(verbose_name='\u957f\u5730\u5740', db_index=True),
        ),
    ]

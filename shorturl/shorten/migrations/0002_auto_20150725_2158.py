# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shorten', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shortenurl',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='shortenurl',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='shortenurl',
            name='code',
            field=models.CharField(max_length=15, verbose_name='\u77ed\u5730\u5740 hash', db_index=True),
        ),
        migrations.AlterField(
            model_name='shortenurl',
            name='long_url',
            field=models.CharField(max_length=1024, verbose_name='\u957f\u5730\u5740', db_index=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ShortenURL',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=15, verbose_name='\u77ed\u5730\u5740 hash', db_column='shorten')),
                ('long_url', models.CharField(max_length=1024, verbose_name='\u957f\u5730\u5740', db_column='expand')),
            ],
            options={
                'db_table': 'url',
            },
        ),
    ]

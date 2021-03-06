# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BookInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('btitle', models.CharField(max_length=20)),
                ('bpub_date', models.DateTimeField()),
                ('bread', models.IntegerField(default=0)),
                ('bcommet', models.IntegerField(default=0)),
                ('isDelete', models.BooleanField(default=False)),
                ('bcontent', tinymce.models.HTMLField()),
            ],
        ),
        migrations.CreateModel(
            name='HeroInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('hname', models.CharField(max_length=20)),
                ('hgender', models.BooleanField(default=1)),
                ('hcontent', models.CharField(max_length=100)),
                ('isDelete', models.BooleanField(default=False)),
                ('hBook', models.ForeignKey(to='booktest.BookInfo')),
            ],
        ),
    ]

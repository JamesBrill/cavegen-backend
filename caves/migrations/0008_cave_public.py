# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-04 21:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caves', '0007_auto_20170101_1351'),
    ]

    operations = [
        migrations.AddField(
            model_name='cave',
            name='public',
            field=models.BooleanField(default=False),
        ),
    ]

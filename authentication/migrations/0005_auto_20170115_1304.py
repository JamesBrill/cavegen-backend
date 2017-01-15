# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-15 13:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_userprofile_liked_caves'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='liked_caves',
            field=models.ManyToManyField(blank=True, to='caves.Cave'),
        ),
    ]

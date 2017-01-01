# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-01 13:51
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('caves', '0006_cave_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cave',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
    ]
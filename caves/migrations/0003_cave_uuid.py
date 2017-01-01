# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-31 18:10
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('caves', '0002_cave_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='cave',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, null=True),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-16 17:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_checklistitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='checklistitem',
            name='item_flag',
            field=models.BooleanField(default=False),
        ),
    ]

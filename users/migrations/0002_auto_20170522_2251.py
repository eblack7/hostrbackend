# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-22 22:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='user',
            name='score',
            field=models.IntegerField(default=0),
        ),
    ]

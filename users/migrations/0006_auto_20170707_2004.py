# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-07 20:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_user_profile_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_link',
            field=models.CharField(blank=True, default='', max_length=2048, null=True),
        ),
    ]

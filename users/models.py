# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=1024)
    full_name = models.CharField(max_length=1024)
    score = models.IntegerField(default=0)
    email = models.CharField(max_length=1024)
    profile_picture_url = models.TextField()
    birthday = models.DateField()
    gender = models.CharField(max_length=10)
    description = models.TextField(default='', null=True, blank=True)
    phone_number = models.CharField(max_length=20)
    fb_access_token = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.full_name
    def __repr__(self):
        return self.full_name

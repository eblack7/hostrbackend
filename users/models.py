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
    birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10)
    description = models.TextField(default='', null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    fb_access_token = models.TextField()
    profile_link = models.CharField(max_length=2048, default='', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.full_name
    def __repr__(self):
        return self.full_name

class FCMToken(models.Model):
    user = models.ForeignKey('User')
    device_token = models.TextField(null=True, blank=True)

    def __str__(self):
        return "FCM Token: {}".format(self.user.full_name)


class Follower(models.Model):
    user = models.ForeignKey('users.User', related_name="user")
    friend = models.ForeignKey('users.User', related_name="friend")
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return "{} - {}".format(self.user.full_name, self.friend.full_name)

    def __repr__(self):
        return "{} - {}".format(self.user.full_name, self.friend.full_name)

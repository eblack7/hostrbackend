# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Event(models.Model):
    event_name = models.CharField(max_length=1024)
    hoster = models.ForeignKey('users.User')
    from_timestamp = models.DateTimeField(auto_now_add=False)
    to_timestamp = models.DateTimeField(auto_now_add=False)
    price = models.DecimalField(max_digits=19, decimal_places=10)
    currency = models.CharField(max_length=10)
    address = models.TextField()
    attending = models.IntegerField(default=1)
    latitude = models.DecimalField(max_digits=19, decimal_places=10)
    longitude = models.DecimalField(max_digits=19, decimal_places=10)
    event_image_url = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.event_name
    def __repr__(self):
        return self.event_name



class Attendee(models.Model):
    event = models.ForeignKey('Event')
    user = models.ForeignKey('users.User')
    attending = models.BooleanField()
    chat_notification = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
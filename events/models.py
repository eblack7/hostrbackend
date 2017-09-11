# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from base64 import b64encode, b64decode

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
    is_private = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.event_name
    def __repr__(self):
        return self.event_name

    class Meta:
        ordering = ['-create_at']



class Attendee(models.Model):
    event = models.ForeignKey('Event')
    user = models.ForeignKey('users.User')
    attending = models.BooleanField()
    chat_notification = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Attendee: {} - \"{}\" ".format(self.user.full_name, self.event.event_name)

    def __repr__(self):
        return "Attendee: {} - \"{}\" ".format(self.user.full_name, self.event.event_name)

class ChecklistItem(models.Model):
    event = models.ForeignKey('Event')
    user = models.ForeignKey('users.User', blank=True, null=True)
    item_name = models.TextField()
    item_flag = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return b64decode(self.item_name)

    def __repr__(self):
        return b64decode(self.item_name)

class Invite(models.Model):
    event = models.ForeignKey('Event', related_name="invite_event")
    user = models.ForeignKey('users.User', related_name="invite_user")
    sent_by = models.ForeignKey('users.User', related_name="invite_sent_by")
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return "Invite: {} from {}".format(self.user.full_name, self.sent_by.full_name)

    class Meta:
        ordering = ['-created_at']
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Driver(models.Model):
    user = models.ForeignKey('users.User')
    event = models.ForeignKey('events.Event')
    vehicle_name = models.CharField(max_length=300)
    vehicle_number = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}-{}'.format(self.user.full_name, self.vehicle_name)
    
    class Meta:
        ordering = ['-created_at']


class Rider(models.Model):
    user = models.ForeignKey('users.User', related_name="rider")
    driver = models.ForeignKey('users.User', related_name="driver")
    event = models.ForeignKey('events.Event')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return "{}-{}".format(self.user.full_name, self.event.event_name)

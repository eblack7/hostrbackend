# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import User, FCMToken, Follower
# Register your models here.
admin.site.register(User)
admin.site.register(FCMToken)
admin.site.register(Follower)
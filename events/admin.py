# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Event, Attendee, ChecklistItem, Invite
# Register your models here.
admin.site.register(Event)
admin.site.register(Attendee)
admin.site.register(ChecklistItem)
admin.site.register(Invite)

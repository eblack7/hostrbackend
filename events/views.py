# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from .models import Event
from users.models import User
import json
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from utils import EventSerializer
# Create your views here.

DATE_FORMATTER = "%Y-%m-%d %H:%M:%S +0000"
eventSerializer = EventSerializer()
def index(request):
    return HttpResponse("Events app.")

@csrf_exempt
def createEvent(request):
    if request.method == 'POST':
        print request.POST.get
        event_name = request.POST.get('event_name')
        hoster = User.objects.get(pk=request.POST.get('hoster_info'))
        from_timestamp = datetime.strptime(request.POST.get('start_timestamp'),
                                            DATE_FORMATTER)
        to_timestamp = datetime.strptime(request.POST.get('end_timestamp'),
                                        DATE_FORMATTER)
        price = float(request.POST.get('price'))
        currency = request.POST.get('currency')
        address = request.POST.get('address')
        latitude = float(request.POST.get('latitude'))
        longitude = float(request.POST.get('longitude'))
        event_image_url = request.POST.get('image_url')
        Event.objects.create(event_name=event_name, hoster=hoster,
                            from_timestamp=from_timestamp,
                            to_timestamp=to_timestamp,
                            price=price,
                            currency=currency,
                            address=address, latitude=latitude,
                            longitude=longitude,
                            event_image_url=event_image_url)
        return HttpResponse(json.dumps({'response': True}),
                            content_type="application/json")
    else:
        return HttpResponse(json.dumps({
        'error': 'invalid request type'
        }),
        content_type="application/json")


@csrf_exempt
def eventFeed(request):
    user_id = request.POST.get('user_id')
    events = Event.objects.all()
    return HttpResponse(EventSerializer.serialize(events),
                        content_type="application/json")

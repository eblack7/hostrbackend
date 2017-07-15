# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json, os
from django.shortcuts import render
from django.http import HttpResponse
from .models import Event, Attendee
from users.models import User, FCMToken
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from .utils import EventSerializer
from pyfcm import FCMNotification
from django.shortcuts import get_object_or_404
from django.db.models import F

# Create your views here.

DATE_FORMATTER = "%Y-%m-%d %H:%M:%S +0000"
eventSerializer = EventSerializer()

FIREBASE_API_KEY = "AAAAVY9gsF8:APA91bFg2vtKqi2NyVG6O-bPBnx98R_snzeJEbTMIJnddOtg3jtCBHztQKYgY6o1LCX1FHK-fZrfWcowWQgOzDt30EwEpbPJg-YrER_FoKLUjlUkLyeWHNj_luQTkMxaTf-AVds_EMCe"

if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
    push_service = FCMNotification(api_key=FIREBASE_API_KEY, env='app_engine')
else:
    push_service = FCMNotification(api_key=FIREBASE_API_KEY)

def index(request):
    return HttpResponse("Events app.")


@csrf_exempt
def createEvent(request):
    if request.method == 'POST':
        print (request.POST.get)
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

@csrf_exempt
def chat_notification(request):
    if request.method == 'POST':
        eventId = request.POST.get('event_id')
        messageTitle = request.POST.get('message_title')
        messageBody = request.POST.get('message_body')

        #get registrationIds
        registrationIds = []
        attendees = Attendee.objects.filter(event_id=eventId,
                                            chat_notification=True)
        for attendee in attendees:
            registrationIds.append(
                FCMToken.objects.get(user_id=attendee.user.pk).device_token)

        result = push_service.notify_multiple_devices(registration_ids=registrationIds,
                                                    message_title=messageTitle,
                                                    message_body=messageBody,
                                                    sound="job-done.m4r")
        return HttpResponse(json.dumps({
            "response": True
            }),
            content_type="application/json")
    else:
        return HttpResponse(json.dumps({
            "error": "invalid request type"
            }),
            content_type="application/json")


@csrf_exempt
def is_attendee(request):
    eventId = request.GET.get('event_id')
    userId = request.GET.get('user_id')
    attendee = get_object_or_404(Attendee, event_id=eventId,
                                user_id=userId)
    return HttpResponse(json.dumps({
        'response': True
        }),
        content_type="application/json")

@csrf_exempt
def attend(request):
    if request.method == 'POST':
        eventId = request.POST.get('event_id')
        userId = request.POST.get('user_id')
        attendee = Attendee.objects.get_or_create(event_id=eventId,
                                                user_id=userId,
                                                attending=True)

        #updating number of people going to the event
        event = Event.objects.get(pk=eventId)
        event.attending = F('attending') + 1
        event.save()

        return HttpResponse(serializers.serialize("json",[attendee[0]])[1:-1],
                            content_type="application/json")
    else:
        return HttpResponse(json.dumps({
            "error": "invalid request type"
            }),
            content_type="application/json")


@csrf_exempt
def edit_chat_notifications(request):
    eventId = request.GET.get('event_id')
    userId = request.GET.get('user_id')
    notifFlag = request.GET.get('notif_flag')
    if eventId and userId and notifFlag is not None:
        attendee = Attendee.objects.get(event_id=eventId, user_id=userId)
        attendee.chat_notification = notifFlag
        print (attendee.save())
        return HttpResponse(json.dumps({
            "response": notifFlag
            }),
            content_type="application/json")
    else:
        return HttpResponse(json.dumps({
            "error": "missing fields"
            }),
            content_type="application/json")
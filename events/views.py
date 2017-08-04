# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json, os, base64, pdb
from django.shortcuts import render
from django.http import HttpResponse
from .models import Event, Attendee, ChecklistItem
from users.models import User, FCMToken
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from .utils import EventSerializer
from pyfcm import FCMNotification
from django.shortcuts import get_object_or_404
from django.db.models import F
from requests import get, post

# Create your views here.

DATE_FORMATTER = "%Y-%m-%d %H:%M:%S +0000"
eventSerializer = EventSerializer()

FIREBASE_API_KEY = "AAAAVY9gsF8:APA91bFg2vtKqi2NyVG6O-bPBnx98R_snzeJEbTMIJnddO" \
                   "tg3jtCBHztQKYgY6o1LCX1FHK-fZrfWcowWQgOzDt30EwEpbPJg-YrER" \
                   "_FoKLUjlUkLyeWHNj_luQTkMxaTf-AVds_EMCe"
NOTIFICATION_SERVER = "http://localhost:8080/send_notif"


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
        event = Event.objects.create(event_name=event_name, hoster=hoster,
                             from_timestamp=from_timestamp,
                             to_timestamp=to_timestamp,
                             price=price,
                             currency=currency,
                             address=address, latitude=latitude,
                             longitude=longitude,
                             event_image_url=event_image_url)
        Attendee.objects.create(event=event, user=hoster, attending=True)
        return HttpResponse(json.dumps({'response': True}),
                            content_type="application/json")
    else:
        return HttpResponse(json.dumps({
            'error': 'invalid request type'
        }),
            content_type="application/json")

@csrf_exempt
def update_event(request):
    if request.method == 'POST':
        event = None
        try:
            event = Event.objects.get(pk=request.POST.get('event_id'))
        except:
            return HttpResponse(json.dumps({
            "error": "event not found"
        }),
        content_type="application/json")

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
        
        
        event.event_name = event_name
        event.from_timestamp = from_timestamp
        event.to_timestamp = to_timestamp
        event.price = price
        event.currency = currency
        event.latitude = latitude
        event.longitude = longitude
        event.event_image_url = event_image_url
        event.save()
        return HttpResponse(json.dumps({
            "response": True
        }), content_type="application/json")


@csrf_exempt
def delete_event(request):
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        event = Event.objects.get(pk=event_id).delete()
        return HttpResponse(json.dumps({
        "response": True
        }),
        content_type="application/json")


@csrf_exempt
def eventFeed(request):
    # user_id = request.POST.get('user_id')
    events = Event.objects.all()
    return HttpResponse(EventSerializer.serialize(events),
                        content_type="application/json")


@csrf_exempt
def chat_notification(request):
    if request.method == 'POST':
        eventId = request.POST.get('event_id')
        messageTitle = request.POST.get('message_title')
        messageBody = request.POST.get('message_body')

        # get registrationIds
        registrationIds = []
        attendees = Attendee.objects.filter(event_id=eventId,
                                            chat_notification=True)
        for attendee in attendees:
            registrationIds.append(
                FCMToken.objects.get(user_id=attendee.user.pk).device_token)

        # additional data
        data = {
            "message": request.POST.get('text'),
            "sender_id": request.POST.get('sender_id'),
            "sender_display_name": request.POST.get('sender_display_name'),
            "event_id": int(request.POST.get('event_id')),
            "timestamp": request.POST.get('timestamp'),
            "text": request.POST.get('text'),
            "type": "group_message"
        }
        result = push_service.notify_multiple_devices(registration_ids=registrationIds,
                                                      message_title=messageTitle,
                                                      message_body=messageBody,
                                                      sound="job-done.m4r",
                                                      badge=1,
                                                      data_message=data)
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

        # updating number of people going to the event
        event = Event.objects.get(pk=eventId)
        event.attending = F('attending') + 1
        event.save()

        user = User.objects.get(pk=userId)
        user.score = F('score') + 1
        user.save()
        event = Event.objects.get(pk=eventId)
        hoster = User.objects.get(pk=event.hoster.pk)
        hoster.score = F('score') + 1
        hoster.save()

        return HttpResponse(serializers.serialize("json", [attendee[0]])[1:-1],
                            content_type="application/json")
    else:
        return HttpResponse(json.dumps({
            "error": "invalid request type"
        }),
            content_type="application/json")


@csrf_exempt
def cancel_attendee(request):
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        user_id = request.POST.get('user_id')
        event = Event.objects.get(pk=event_id)
        event.attending = F('attending') - 1
        event.save()
        attendee = Attendee.objects.get(event_id=event_id, user_id=user_id).delete()
        return HttpResponse(json.dumps({
            "response": True
        }),
            content_type="application/json")


@csrf_exempt
def edit_chat_notifications(request):
    """
    Args:
        request (DjangoRequest): general request object

    request-parameters: POST
        @eventId : (Event Object)
        @userId (User Model)
        @notifFlag (boolean)
    """
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


@csrf_exempt
def new_checklist_item(request):
    '''
    request-parameters: POST
        @eventId
        @itemName
    '''
    if request.method == 'POST':
        eventId = request.POST.get('event_id')
        itemName = base64.b64encode(request.POST.get('item_name').encode('utf-8'))
        new_item = ChecklistItem.objects.create(event_id=eventId,
                                                item_name=itemName)
        return HttpResponse(serializers.serialize("json", [new_item])[1:-1],
                            content_type="application/json")
    else:
        return HttpResponse(json.dumps({
            "error": "invalid request type."
        }),
            content_type="application/json")


@csrf_exempt
def change_checklist_item_state(request):
    '''
    request-parameters: POST
        @itemId
        @userId
        @itemFlag (boolean)
    '''
    if request.method == 'POST':
        print (request.POST)
        payload = json.loads(request.body)
        print (payload)
        item_id = payload["item_id"]
        user_id = payload["user_id"]
        item = ChecklistItem.objects.get(pk=item_id)
        if item.user is None:
            item.user = User.objects.get(pk=user_id)
        elif user_id is None:
            item.user = None
        else:
            item.user.pk = user_id
        item.item_flag = True if item.item_flag is False else False
        # item.item_flag = itemFlag
        item.save()
        return HttpResponse(json.dumps({
            "response": True
        }),
            content_type="application/json")
    else:
        return HttpResponse(json.dumps({
            "error": "invalid request type."
        }),
            content_type="application/json")


@csrf_exempt
def get_items(request):
    """
    request-parameters:
        @eventId
    """
    eventId = request.GET.get('event_id')
    items = ChecklistItem.objects.filter(event_id=eventId)
    response = []
    for item in items:
        response.append({
            "pk": item.pk,
            "fields": {
                "event": item.event.pk,
                "user": item.user.full_name if item.user is not None else None,
                "item_name": base64.b64decode(item.item_name).decode('utf-8'),
                "item_flag": item.item_flag
            }
        })
    return HttpResponse(json.dumps(response),
                        content_type="application/json")


@csrf_exempt
def new_send_notification(request):
    device_tokens = list()
    for token in FCMToken.objects.filter(user_id=6):
        device_tokens.append(token.device_token)

    message_data = {
        "device_tokens": device_tokens,
        "message_payload": {
            "title": "Message Title",
            "body": "Message Body"
        }
    }
    # headers = {'Content-type': 'application/json'}
    try:
        r = post("http://localhost:8080/send_not", data=json.dumps(message_data))
    except:
        return HttpResponse(json.dumps({'error': 'please try later.'}), content_type="application/json")
    return HttpResponse(r.content)

@csrf_exempt
def my_events(request):
    user_id = request.GET.get("id")
    attending = Attendee.objects.filter(user_id=user_id)
    events = []
    for attendee in attending:
        events.append(Event.objects.get(pk=attendee.event.pk))
    return HttpResponse(EventSerializer.serialize(events),
                        content_type="application/json")

@csrf_exempt
def list_attendees(request):
    event_id = request.GET.get('id')
    attendees = Attendee.objects.filter(event_id=event_id)
    response = []
    for attendee in attendees:
        response.append(
            json.loads(serializers.serialize("json", [attendee.user])[1:-1])
        )
    return HttpResponse(json.dumps(response), content_type="application/json")

"""
All event app views in this file
"""
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import os
import base64
from datetime import datetime

from pyfcm import FCMNotification
from django.http import HttpResponse
from django.core import serializers
from django.db.models import F
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from users.models import User, FCMToken, Follower

from .models import Event, Attendee, ChecklistItem
from .utils import EventSerializer

# Create your views here.

DATE_FORMATTER = "%Y-%m-%d %H:%M:%S +0000"

FIREBASE_API_KEY = "AAAAVY9gsF8:APA91bFg2vtKqi2NyVG6O-bPBnx98R_snzeJEbTMIJnddO" \
                   "tg3jtCBHztQKYgY6o1LCX1FHK-fZrfWcowWQgOzDt30EwEpbPJg-YrER" \
                   "_FoKLUjlUkLyeWHNj_luQTkMxaTf-AVds_EMCe"
NOTIFICATION_SERVER = "http://localhost:8080/send_notif"


if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
    PUSH_SERVICE = FCMNotification(api_key=FIREBASE_API_KEY, env='app_engine')
else:
    PUSH_SERVICE = FCMNotification(api_key=FIREBASE_API_KEY)


def index(request):
    '''
    Test index route
    '''
    return HttpResponse('Events app: {}'.format(request.body))


@csrf_exempt
def createEvent(request):
    """
    This view creates the entire event and saves the instance to the database
    """
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
        is_private = bool(int(request.POST.get('is_private')))
        event_image_url = request.POST.get('image_url')
        # Creating new event
        event = Event.objects.create(event_name=event_name, hoster=hoster,
                                     from_timestamp=from_timestamp,
                                     to_timestamp=to_timestamp,
                                     price=price,
                                     currency=currency,
                                     address=address, latitude=latitude,
                                     longitude=longitude,
                                     event_image_url=event_image_url,
                                     is_private=is_private)


        # Adding the user to his event as an attendee
        Attendee.objects.create(event=event, user=hoster, attending=True)


        return HttpResponse(json.dumps({'response': True}),
                            content_type="application/json")



    # Default response if any other request type is sent
    return HttpResponse(json.dumps({'error': 'invalid request type'}),
                        content_type="application/json")

@csrf_exempt
def update_event(request):
    '''
    requests-aruments:
        same as create_event
    '''
    if request.method == 'POST':
        event = None
        event_id = request.POST.get('event_id')
        event = get_object_or_404(Event, pk=event_id)

        print request.POST.get

        event_name = request.POST.get('event_name')
        hoster = User.objects.get(pk=request.POST.get('hoster_info'))
        print hoster.full_name
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
        is_private = request.POST.get('is_private')


        event.event_name = event_name
        event.from_timestamp = from_timestamp
        event.to_timestamp = to_timestamp
        event.address = address
        event.price = price
        event.currency = currency
        event.latitude = latitude
        event.longitude = longitude
        event.event_image_url = event_image_url
        event.is_private = is_private
        event.save()
        return HttpResponse(json.dumps({
            "response": True
        }), content_type="application/json")


@csrf_exempt
def delete_event(request):
    '''
    request-arguments:
        event_id
    '''
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        Event.objects.get(pk=event_id).delete()
        return HttpResponse(json.dumps({"response": True}),
                            content_type="application/json")


@csrf_exempt
def event_feed(request):
    '''
    request-arguments:
        user_id
    '''
    # user_id = request.POST.get('user_id')
    # getting all events except the ones that are over
    print '{}'.format(request.body)
    now = timezone.now()
    events = Event.objects.exclude(to_timestamp__lt=now) \
                  .exclude(is_private=True) \
                  .order_by('-from_timestamp', 'to_timestamp')

    # Access users private events
    # Add them to events feed and sort them based on the timestamp

    return HttpResponse(EventSerializer.serialize(events),
                        content_type="application/json")


@csrf_exempt
def chat_notification(request):
    '''
    request-arguments:
        event_id,
        message_title,
        message_body
    '''
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        message_title = request.POST.get('message_title')
        message_body = request.POST.get('message_body')

        # get registrationIds
        registrationIds = []
        attendees = Attendee.objects.filter(event_id=event_id,
                                            chat_notification=True)
        for attendee in attendees:
            registrationIds.append(
                FCMToken.objects.get(user_id=attendee.user.pk).device_token)

        # Additional notification data
        data = {
            "message": request.POST.get('text'),
            "sender_id": request.POST.get('sender_id'),
            "sender_display_name": request.POST.get('sender_display_name'),
            "event_id": int(request.POST.get('event_id')),
            "timestamp": request.POST.get('timestamp'),
            "text": request.POST.get('text'),
            "type": "group_message"
        }

        # Sending notification using FCM to all registered devices
        PUSH_SERVICE.notify_multiple_devices(registration_ids=registrationIds,
                                             message_title=message_title,
                                             message_body=message_body,
                                             sound="job-done.m4r",
                                             badge=1,
                                             data_message=data)

        return HttpResponse(json.dumps({"response": True}),
                            content_type="application/json")


    # Default response for invalid request type.
    return HttpResponse(json.dumps({"error": "invalid request type"}),
                        content_type="application/json")


@csrf_exempt
def is_attendee(request):
    '''
    request-arguments:
        event_id,
        user_id
    '''
    event_id = request.GET.get('event_id')
    user_id = request.GET.get('user_id')
    attendee = get_object_or_404(Attendee, event_id=event_id,
                                 user_id=user_id)


    return HttpResponse(json.dumps({'response': True, \
                        'attendee': attendee.attending}),
                        content_type="application/json")


@csrf_exempt
def attend(request):
    '''
    request-arguments:
        event_id,
        user_id
    '''
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        user_id = request.POST.get('user_id')
        attendee = Attendee.objects.get_or_create(event_id=event_id,
                                                  user_id=user_id,
                                                  attending=True)

        # Updating number of people going to the event
        event = Event.objects.get(pk=event_id)
        event.attending = F('attending') + 1
        event.save()

        # Updating user score and hoster score
        user = User.objects.get(pk=user_id)
        user.score = F('score') + 1
        user.save()
        event = Event.objects.get(pk=event_id)
        hoster = User.objects.get(pk=event.hoster.pk)
        hoster.score = F('score') + 1
        hoster.save()

        return HttpResponse(serializers.serialize("json", [attendee[0]])[1:-1],
                            content_type="application/json")



    return HttpResponse(json.dumps({"error": "invalid request type"}),
                        content_type="application/json")


@csrf_exempt
def cancel_attendee(request):
    '''
    request-arguments:
    event_id,
    user_id
    '''
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        user_id = request.POST.get('user_id')
        event = Event.objects.get(pk=event_id)
        event.attending = F('attending') - 1
        event.save()
        Attendee.objects.get(event_id=event_id, user_id=user_id).delete()


        return HttpResponse(json.dumps({"response": True}),
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
    event_id = request.GET.get('event_id')
    user_id = request.GET.get('user_id')
    notif_flag = request.GET.get('notif_flag')
    if event_id and user_id and notif_flag is not None:
        attendee = Attendee.objects.get(event_id=event_id, user_id=user_id)
        attendee.chat_notification = notif_flag
        print attendee.save()


        return HttpResponse(json.dumps({"response": notif_flag}),
                            content_type="application/json")


    return HttpResponse(json.dumps({"error": "missing fields"}),
                        content_type="application/json")


@csrf_exempt
def new_checklist_item(request):
    '''
    request-parameters: POST
        @eventId
        @itemName
    '''
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        item_name = base64.b64encode(request.POST.get('item_name').encode('utf-8'))
        new_item = ChecklistItem.objects.create(event_id=event_id,
                                                item_name=item_name)
        #Send notification regarding new CheckListItem
        event = Event.objects.get(pk=event_id)
        attendees = Attendee.objects.filter(event=event)
        fcm_tokens = [FCMToken.objects.get(user=a.user).device_token for a in attendees]
        message_body = "New Item \"{}\" added to Checklist".format(base64.b64decode(item_name))
        PUSH_SERVICE \
            .notify_multiple_devices(registration_ids=fcm_tokens,
                                     message_title=event.event_name,
                                     message_body=message_body,
                                     sound="job-done.m4r",
                                     badge=1)
        return HttpResponse(serializers.serialize("json", [new_item])[1:-1],
                            content_type="application/json")


    return HttpResponse(json.dumps({"error": "invalid request type."}),
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
        print request.POST
        payload = json.loads(request.body)
        print payload
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

        return HttpResponse(json.dumps({"response": True}),
                            content_type="application/json")

    else:
        return HttpResponse(json.dumps({"error": "invalid request type."}),
                            content_type="application/json")


@csrf_exempt
def get_items(request):
    """
    request-parameters:
        @eventId
    """
    event_id = request.GET.get('event_id')
    items = ChecklistItem.objects.filter(event_id=event_id)
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
def deleteItem(request):
    """
    deletes a specific checklist item
    """
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        item = ChecklistItem.objects.get(pk=item_id)
        item.delete()
        return HttpResponse(json.dumps({'response': True}), content_type="application/json")

@csrf_exempt
def my_events(request):
    '''
    request-arguments:
        user_id as id
    '''
    user_id = request.GET.get("id")
    attending = Attendee.objects.filter(user_id=user_id)
    events = []
    for attendee in attending:
        events.append(Event.objects.get(pk=attendee.event.pk))
    return HttpResponse(EventSerializer.serialize(events),
                        content_type="application/json")

@csrf_exempt
def list_attendees(request):
    '''
    request-arguments:
        event_id as id
    '''
    event_id = request.GET.get('id')
    attendees = Attendee.objects.filter(event_id=event_id)
    response = []
    for attendee in attendees:
        response.append(
            json.loads(serializers.serialize("json", [attendee.user])[1:-1])
        )
    return HttpResponse(json.dumps(response), content_type="application/json")


@csrf_exempt
def list_invitees(request):
    """
    this view lists all the invitees that could be possible for
    given user """
    if request.method == 'GET':
        event_id = request.GET.get("event_id")
        print 'Listing invitees for: {}'.format(event_id)
        user_id = request.GET.get("user_id")

        invitees = []
        # Get all the followers and following people of User object
        followers = Follower.objects.filter(friend_id=user_id)
        if followers.count() > 0:
            for follower in followers:
                invitees.append(
                    json.loads(serializers.serialize("json", [follower.user])[1:-1])
                )

        return HttpResponse(json.dumps(invitees), content_type="application/json")


    # Default HttpResponse in case of invalid request
    return HttpResponse(json.dumps({"error": "invalid request type."}),
                        content_type="application/json")


@csrf_exempt
def invite_connection(request):
    """
    request-params:
    event_id,
    invite_user_id,
    invite_sent_by
    """
    if request.method == 'POST':
        payload = json.loads(request.body)
        event_id = payload['event_id']
        event = Event.objects.get(pk=event_id)

        try:
            invite_sent_by = payload['invite_sent_by']
            invite_sent_by = User.objects.get(pk=invite_sent_by)
        except KeyError:
            invite_sent_by = event.hoster

        # If event is private add the user to the event directly.
        if event.is_private:
            private_message_body = 'Added to private event \"{}\" by '\
                                    '{}'.format(event.event_name,
                                                invite_sent_by.full_name)

            device_tokens = []
            for user in payload['selected_ids']:
                Attendee.objects.create(event=event, user_id=user,
                                        attending=True)

                # Updating event with new attendee count
                event.attending = F('attending') + 1
                event.save()

                # Send a notification confirming invite
                token = FCMToken.objects.get(user_id=user).device_token
                device_tokens.append(token)

            # Sending push message to all devices
            PUSH_SERVICE \
            .notify_multiple_devices(registration_ids=device_tokens,
                                     message_title="New Invite",
                                     message_body=private_message_body,
                                     sound="job-done.m4r",
                                     badge=1)

            return HttpResponse(json.dumps({'response': True}),
                                content_type="application/json")


        message_body = "\'" + event.event_name + "\' from " + invite_sent_by.full_name
        tokens = []
        for user_id in payload["selected_ids"]:
            # add a new invite object into the database to notify the user of his invites
            token = FCMToken.objects.get(user_id=user_id).device_token
            tokens.append(token)

        PUSH_SERVICE.notify_multiple_devices(registration_ids=tokens,
                                             message_title="New Invite",
                                             message_body=message_body,
                                             sound="job-done.m4r",
                                             badge=1)

        # Default server response
        return HttpResponse(json.dumps({"response": True}),
                            content_type="application/json")

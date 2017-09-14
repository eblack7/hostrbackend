# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from events.utils import EventSerializer
from events.models import Event
from users.models import User
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def index():
    '''
    sample index request
    '''
    return HttpResponse(json.dumps({'response': 'index route'}),
                        content_type="application/json")

@csrf_exempt
def search_events(request):
    '''
    request-parameters:
        search_query: a string query for searching through events table
    '''
    if request.method == 'POST':
        payload = json.loads(request.body)
        events = Event.objects.filter(event_name__search=payload['search_query'])
        return HttpResponse(EventSerializer.serialize(events), content_type="application/json")


    return HttpResponse(json.dumps({'error': 'invalid request type.'}),
                        content_type="application/json")

@csrf_exempt
def search_users(request):
    '''
    request-parameters:
        search_query: a string query for searching through users table
    '''
    if request.method == 'POST':
        payload = json.loads(request.body)
        users = User.objects.filter(full_name__search=payload['search_query'])
        return HttpResponse(serializers.serialize("json", users), content_type="application/json")


    return HttpResponse(json.dumps({'error': 'invalid request type.'}),
                        content_type="application/json")
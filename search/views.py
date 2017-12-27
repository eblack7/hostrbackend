# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.core import serializers
from django.http import HttpResponse
from django.views import generic

import events
import users


# Create your views here.
def index():
    '''
    sample index request
    '''
    return HttpResponse(json.dumps({'response': 'index route'}),
                        content_type="application/json")

class SearchEvents(generic.View):
    """ search for events in database. """
    def post(self, request):
        """ Runs when a POST request is sent to the search application. """
        payload = json.loads(request.body)
        search_events = events.models.Event.objects \
                                    .filter(event_name__search=payload['search_query'])
        return HttpResponse(events.utils.EventSerializer.serialize(search_events),
                            content_type="application/json")

class SearchUsers(generic.View):
    """ search for users in database. """
    def post(self, request):
        """ runs when a post request is sent to the search application. """
        payload = json.loads(request.body)
        search_users = users.models.User.objects.filter(full_name__search=payload['search_query'])
        return HttpResponse(serializers.serialize("json", search_users),
                            content_type="application/json")

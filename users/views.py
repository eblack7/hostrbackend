# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
import json
from .models import User
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def index(request):
    return HttpResponse(json.dumps({'response': 'Welcome to users app'}),
                        content_type="application/json")


@csrf_exempt
def all(request):
    users = User.objects.all()
    return HttpResponse(serializers.serialize("json", users),
                        content_type="application/json")

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
import json
from .models import User
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from .models import User


# Create your views here.
def index(request):
    return HttpResponse(json.dumps({'response': 'Welcome to users app'}),
                        content_type="application/json")


@csrf_exempt
def all(request):
    users = User.objects.all()
    return HttpResponse(serializers.serialize("json", users),
                        content_type="application/json")


@csrf_exempt
def signUp(request):
    '''
    User sign up view.
    All signup realted stuff is handled here.
    :param request: 
    :return HttpResponse: 
    '''
    if request.method == 'POST':
        full_name = request.POST.get('name')
        profile_picture_url = request.POST.get('profile_picture_url')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        birthday = datetime.strptime(request.POST.get('birthday'), '%m/%d/%Y').date()
        phone_number = ""
        username = email.split('@')[0]

        new_user = User(username=username, full_name=full_name, email=email, profile_picture_url=profile_picture_url,
                        birthday=birthday, gender=gender, phone_number=phone_number,
                        fb_access_token=request.POST.get('fb_access_token'))
        new_user.save()
        return HttpResponse(serializers.serialize("json", [new_user])[1:-1], content_type="application/json")

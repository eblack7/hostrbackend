# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import json
from .models import User
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from .models import User, FCMToken, Follower


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
    All signup related stuff is handled here.
    :param request:
    :return HttpResponse:
    '''
    if request.method == 'POST':
        # check if email already exists
        # use django get or create instance here

        try:
            user = User.objects.get(email=request.POST.get('email'))
            user.fb_access_token = request.POST.get('fb_access_token')
            user.save()
            return HttpResponse(serializers.serialize("json", [user])[1:-1],
                                content_type="application/json")
        except MultipleObjectsReturned:
            user = User.objects.filter(email=request.POST.get('email'))
            if len(user) > 1:
                user = user[0]
            return HttpResponse(serializers.serialize("json", user)[1:-1],
                                content_type="application/json")
        except ObjectDoesNotExist:
            pass


        full_name = request.POST.get('name')
        profile_picture_url = request.POST.get('profile_picture_url')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        #birthday = datetime.strptime(request.POST.get('birthday'), '%m/%d/%Y').date()
        phone_number = ""
        username = email.split('@')[0]

        new_user = User(username=username, full_name=full_name, email=email,
                        profile_picture_url=profile_picture_url,
                        gender=gender, phone_number=phone_number,
                        fb_access_token=request.POST.get('fb_access_token'))
        new_user.save()
        return HttpResponse(serializers.serialize("json", [new_user])[1:-1],
                            content_type="application/json")

@csrf_exempt
def updateProfile(request):
    '''
    This view updates all parameters of the User model.
    '''
    #print request.body
    if request.method == 'POST':
        # update_payload = json.loads(request.body)
        update_payload = request.POST
        print (update_payload)
        try:
            user = User.objects.get(pk=update_payload.get('user_id'))
            #update all user attributes
            user.username = update_payload['username']
            user.full_name = update_payload['full_name']
            user.email = update_payload['email']
            user.profile_picture_url = update_payload['profile_picture_url']
            user.description = update_payload['description']
            user.profile_link = update_payload['profile_link']
            user.phone_number = update_payload['phone_number']
            user.save()
            # Returning a confirmation if update was successful.
            return HttpResponse(json.dumps({
            'response': True
            }),
            content_type="application/json")
        except ObjectDoesNotExist:
            return HttpResponse(json.dumps({
            'error': 'user not found'
            }),
            content_type="application/json")
    else:
        return HttpResponse(json.dumps({
        'error': 'invalid request type'
        }),
        content_type="application/json")


@csrf_exempt
def get_or_create_fcm_tokens(request):
    if request.method == 'POST':
        Id = request.POST.get('id')
        device_token = request.POST.get('device_token')
        fcm_token = FCMToken.objects.get_or_create(user_id=Id)
        fcm_token[0].device_token = device_token
        fcm_token[0].save()
        return HttpResponse(json.dumps({
            "id": fcm_token[0].user.pk,
            "device_token": fcm_token[0].device_token
            }),
        content_type="application/json")
    else:
        return HttpResponse(json.dumps({
            "error": "invalid request type"
            }),
        content_type="application/json")


@csrf_exempt
def follow(request):
    if request.method == 'POST':
        user_id = request.POST.get("user_id")
        friend_id = request.POST.get("friend_id")
        Follower.objects.create(user_id=user_id, friend_id=friend_id)
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
def is_follower(request):
    user_id = request.GET.get("user_id")
    friend_id = request.GET.get("friend_id")
    follower = get_object_or_404(Follower, user_id=user_id, friend_id=friend_id)
    return HttpResponse(serializers.serialize("json", [follower]),
                        content_type="application/json")

@csrf_exempt
def unfollow(request):
    if request.method == 'POST':
        user_id = request.POST.get("user_id")
        friend_id = request.POST.get("friend_id")
        Follower.objects.get(user_id=user_id, friend_id=friend_id).delete()
        return HttpResponse(json.dumps({
            "response": True
        }),
            content_type="application/json")


@csrf_exempt
def get_score(request):
    user_id = request.GET.get("user_id")
    score = User.objects.get(pk=user_id).score
    return HttpResponse(json.dumps({
        "score": score
    }),
    content_type="application/json")

@csrf_exempt
def get_user_data(request):
    user = User.objects.get(pk=request.GET.get("id"))
    return HttpResponse(serializers.serialize("json", [user])[1:-1],
                        content_type="application/json")

@csrf_exempt
def get_stats(request):
    '''
    This view gets the current users stats
    request-arguments:
        user_id
    '''
    following = Follower.objects.filter(user_id=request.GET.get("id")).count()
    followers = Follower.objects.filter(friend_id=request.GET.get("id")).count()


    return HttpResponse(json.dumps({"followers": followers, \
                        "following": following}),
                        content_type="application/json")


@csrf_exempt
def get_network(request):
    '''
    request-arguments:
        user_id
    '''
    if request.method == 'POST':
        payload = json.loads(request.body)
        user_id = payload['user_id']
        
        # Get followers
        followers = Follower.objects.filter(user_id=user_id) \
                    .order_by('-created_at')

        # Get following
        following = Follower.objects.filter(friend_id=user_id) \
                    .order_by('-created_at')

        response = {
            "followers": [],
            "following": []
        }

        for user in followers:
            response["followers"].append(
                json.loads(serializers.serialize("json", [user.friend])[1:-1])
            )

        for user in following:
            response["following"].append(
                json.loads(serializers.serialize("json", [user.user])[1:-1])
            )

        return HttpResponse(json.dumps(response),
                            content_type="application/json")

    return HttpResponse(json.dumps({"error": "invalid request type."}),
                        content_type="application/json")

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
import firebase_admin
from firebase_admin import credentials
# Create your views here.
def index(request):
	return HttpResponse("Welcome to users")
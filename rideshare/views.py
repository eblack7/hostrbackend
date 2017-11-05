"""
All Rideshare Django views in this file.
"""
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse

# Create your views here.
def index(request):
    """
    A place holder index view for django
    """
    print request
    return HttpResponse("Ride share.",
                        content_type="application/json")
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import TemplateView, View
from django.http import HttpResponse
# Create your views here.

class IndexView(TemplateView):
    """ Index view template for system app """
    template_name = "system/index.html"

class LoginView(View):
    """ Sameple login view"""
    def post(self, request):
        return HttpResponse("lol")
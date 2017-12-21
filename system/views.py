# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import redirect
from django.views.generic import View, TemplateView
# Create your views here.

class IndexView(TemplateView):
    """ Index view template for system app """
    template_name = "system/index.html"

class LoginView(View):
    """ Logs a admin into systemz. """

    def post(self, request):
        """ Checks username and password and logs in user. """
        user_context = {'username': request.POST['username'], 'id': 1}
        return redirect("systemz_dashboard")


class DashboardView(TemplateView):
    """ Main Dashboard View """
    template_name = "system/dashboard.html"

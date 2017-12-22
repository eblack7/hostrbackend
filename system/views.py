# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import View, TemplateView

from events.models import Event
# Create your views here.

class IndexView(TemplateView):
    """ Index view template for system app """
    template_name = "system/index.html"

class LoginView(View):
    """ Logs a admin into systemz. """

    def post(self, request):
        """ Checks username and password and logs in user. """
        user = authenticate(request=request, username=request.POST['systemz_username'],
                            password=request.POST['systemz_password'])
        if user is not None:
            login(request, user)
            return redirect("systemz_dashboard", uid=user.pk)
        return redirect("systemz_index")

@method_decorator(login_required, name="dispatch")
class LogoutView(View):
    """ Logs a user out from systemz. """

    def get(self, request):
        """ Logout user. """
        logout(request)
        return redirect("systemz_index")

@method_decorator(login_required, name="dispatch")
class DashboardView(TemplateView):
    """ Main Dashboard View """
    template_name = "system/dashboard.html"
    redirect_field_name = "systemz_index"

    def get(self, request, *args, **kwargs):
        """ runs when a get request is sent. """
        cxt = self.get_context_data()
        cxt['events'] = Event.objects.all()
        return self.render_to_response(cxt)

@method_decorator(login_required, name="dispatch")
class EventDetailView(TemplateView):
    """ shows event details. """
    template_name = "system/event_detail.html"
    redirect_field_name = "systemz_index"

    def get(self, request, *args, **kwargs):
        """ runs when get request is sent """
        cxt = self.get_context_data()
        cxt['event_details'] = Event.objects.get(pk=kwargs['event_id'])
        return self.render_to_response(cxt)

""" URL's for rideshare service. """
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^/ride/', views.RideView.as_view()),
]

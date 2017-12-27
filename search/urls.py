""" Search app URL's """
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'search_events/', views.SearchEvents.as_view()),
    url(r'search_users/', views.SearchUsers.as_view())
]

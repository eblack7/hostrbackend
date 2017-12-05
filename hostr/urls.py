"""
Main URL routing file
"""
from django.contrib import admin
from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^users/', include('users.urls')),
    url(r'^events/', include('events.urls')),
    url(r'^search/', include('search.urls')),
    url(r'^privacy/', views.privacy),
]

from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^create_event/', views.createEvent),
    url(r'event_feed/', views.eventFeed),
]

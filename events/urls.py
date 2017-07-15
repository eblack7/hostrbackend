from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^create_event/', views.createEvent),
    url(r'event_feed/', views.eventFeed),
    url(r'chat_notification/', views.chat_notification),
    url(r'is_attendee/', views.is_attendee),
    url(r'attend/', views.attend),
    url(r'edit_chat_notifications/', views.edit_chat_notifications),
]

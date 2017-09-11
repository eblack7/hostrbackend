from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'search_events', views.search_events),
    url(r'search_users/', views.search_users),
]

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^all/', views.all),
    url(r'^signup/', views.signUp),
    url(r'^update_profile/', views.updateProfile),
]

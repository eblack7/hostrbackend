from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^all/', views.all),
    url(r'^signup/', views.signUp),
    url(r'^update_profile/', views.updateProfile),
    url(r'^fcm_token/', views.get_or_create_fcm_tokens),
    url(r'^follow/', views.follow),
    url(r'^is_follower', views.is_follower),
    url(r'^unfollow/', views.unfollow),
    url(r'^get_data/', views.get_user_data),
    url(r'^stats/', views.get_stats),
    url(r'^get_score/', views.get_score),
]

""" Urls for system app """
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view()),
    url(r'^login/', views.LoginView.as_view(), name="systemz_login"),
    url(r'dashboard/', views.DashboardView.as_view(), name="systemz_dashboard"),
]

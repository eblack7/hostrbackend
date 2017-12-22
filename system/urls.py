""" Urls for system app """
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name="systemz_index"),
    url(r'^login/', views.LoginView.as_view(), name="systemz_login"),
    url(r'^logout/', views.LogoutView.as_view(), name="systemz_logout"),
    url(r'^event/(?P<event_id>[0-9]+)', views.EventDetailView.as_view(), name="systemz_event_detail"),
    url(r'^(?P<uid>[0-9]+)/dashboard$', views.DashboardView.as_view(), name="systemz_dashboard")
]

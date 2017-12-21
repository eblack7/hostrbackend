"""
Main URL routing file
"""
from django.contrib import admin
from django.conf.urls import include, url
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage


from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^users/', include('users.urls')),
    url(r'^events/', include('events.urls')),
    url(r'^search/', include('search.urls')),
    url(r'^system/', include('system.urls')),
    url(r'^privacy/', views.privacy),
   
    # Favicon RedirectView
    url(r'^favicon.ico$',
        RedirectView.as_view(url=staticfiles_storage.url('favicon.ico'),
                            permanent=False), name="favicon")
]

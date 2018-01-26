from django.conf.urls import include, url
from django.contrib import admin
from . import views
urlpatterns = [url(r'^$', views.index),
               url(r'^amazon$', views.prod),
               url(r'^click$', views.click),
               url(r'^rate$', views.rate),
               ]
                # url(r'^review$', views.highlight)

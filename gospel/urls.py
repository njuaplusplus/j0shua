#!/usr/bin/python
# coding=utf-8
from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /gospel/
    url(r'^$', views.index, name='index'),
    url(r'^contact-us/$', views.contact_us, name='contact_us'),
]
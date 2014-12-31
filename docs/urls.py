#!/usr/local/bin/python
# coding=utf-8

from django.conf.urls import patterns, url

from docs import views

urlpatterns = patterns('',
    url(r'^(?P<doc_name>[A-Za-z0-9\-]+)/$', views.docs_view, name='docs_view'),
)

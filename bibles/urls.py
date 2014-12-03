#!/usr/local/bin/python
# coding=utf-8

from django.conf.urls import patterns, url

from bibles import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^bible/$', views.bible, name='bible'),
    # For ajax, return bible json array
    url(r'^json/bible/(?P<book_id>\d+)/(?P<chapternum>\d+)/$', views.json_bible, name='json_bible'),
    url(r'^accounts/login/$', views.login_view, name='login_view'),
    url(r'^accounts/logout/$', views.logout_view, name='logout_view'),
    url(r'^accounts/register/$', views.register_view, name='register_view'),
)

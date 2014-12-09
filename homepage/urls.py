#!/usr/bin/python
# coding=utf-8

from django.conf.urls import patterns, url

from homepage import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about_view, name='about_view'),
    url(r'^accounts/login/$', views.login_view, name='login_view'),
    url(r'^accounts/logout/$', views.logout_view, name='logout_view'),
    url(r'^accounts/register/$', views.register_view, name='register_view'),
)

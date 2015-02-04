#!/usr/local/bin/python
# coding=utf-8

from django.conf.urls import patterns, url

from myadmin import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^users/$', views.users_view, name='users_view'),
    url(r'^weekly_hymns/$', views.weekly_hymns_view, name='weekly_hymns_view'),
    url(r'^daily_verses/$', views.daily_verses_view, name='daily_verses_view'),
    url(r'^weekly_verses/$', views.weekly_verses_view, name='weekly_verses_view'),
    url(r'^weekly_readings/$', views.weekly_readings_view, name='weekly_readings_view'),
    url(r'^weekly_recitations/$', views.weekly_recitations_view, name='weekly_recitations_view'),
    url(r'^write-post/$', views.write_post_view, name='write_post_view'),
    url(r'^edit-post/(?P<post_id>\d+)/$', views.edit_post_view, name='edit_post_view'),
    url(r'^accounts/login/$', views.login_view, name='login_view'),
    url(r'^accounts/logout/$', views.logout_view, name='logout_view'),
)

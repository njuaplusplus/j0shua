#!/usr/bin/python
# coding=utf-8

from django.conf.urls import url, handler404

from homepage import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about_view, name='about_view'),
    url(r'^accounts/login/$', views.login_view, name='login_view'),
    url(r'^accounts/login/wechat/$', views.wechat_login_view, name='wechat_login_view'),
    url(r'^accounts/logout/$', views.logout_view, name='logout_view'),
    # url(r'^accounts/register/$', views.register_view, name='register_view'),
    url(r'^print_request/$', views.print_request, name='print_request'),
]

handler404 = 'homepage.views.page_not_found_view'

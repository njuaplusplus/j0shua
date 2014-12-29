#!/usr/local/bin/python
# coding=utf-8

from django.conf.urls import patterns, url

from blog import views

urlpatterns = patterns('',
    url('^$', views.index, name="index"),
    url('^page/(?P<page_num>[\d]+)/$', views.index_page, name="index_page"),
    url('^archive/(?P<year>[\d]+)/(?P<month>[\d]+)/$', views.date_archive, name="blog-date-archive"),
    url('^archive/(?P<slug>[-\w]+)/$', views.category_archive, name="blog-category-archive"),
    url('^post/(?P<slug>[-\w]+)/$', views.single, name="single_post"),
)

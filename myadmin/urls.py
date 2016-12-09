#!/usr/local/bin/python
# coding=utf-8

from django.conf.urls import url

from myadmin import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^users/$', views.users_view, name='users_view'),
    url(r'^weekly-hymns/$', views.weekly_hymns_view, name='weekly_hymns_view'),
    url(r'^daily-verses/$', views.daily_verses_view, name='daily_verses_view'),
    url(r'^weekly-verses/$', views.weekly_verses_view, name='weekly_verses_view'),
    url(r'^weekly-readings/$', views.weekly_readings_view, name='weekly_readings_view'),
    url(r'^weekly-recitations/$', views.weekly_recitations_view, name='weekly_recitations_view'),
    # For blogs
    url(r'all-articles/$', views.all_articles_view, name='all_articles_view'),
    url(r'^write-article/$', views.write_article_view, name='write_article_view'),
    url(r'^edit-article/(?P<article_id>\d+)/$', views.edit_article_view, name='edit_article_view'),

    url(r'^accounts/login/$', views.login_view, name='login_view'),
    url(r'^accounts/logout/$', views.logout_view, name='logout_view'),
    url(r'^user-profile/$', views.user_profile_view, name='user_profile_view'),
    url(r'^upload-hymn/$', views.upload_hymn_view, name='upload_hymn_view'),
    url(r'^upload-hymn-score/(?P<hymn_id>\d+)/$', views.upload_hymn_score_view, name='upload_hymn_score_view'),
    url(r'^upload-hymn-score-callback/$', views.upload_hymn_score_callback, name='upload_hymn_score_callback'),
    url(r'^upload-score-token/$', views.upload_score_token, name='upload_score_token'),
    url(r'^edit-hymn/(?P<hymn_id>\d+)/$', views.edit_hymn_view, name='edit_hymn_view'),
    url(r'^hymns/$', views.hymns_view, name='hymns_view'),
]

#!/usr/bin/python
# coding=utf-8
from django.conf.urls import patterns, url

from hymns import views

urlpatterns = patterns('',
    # ex: /hymns/
    url(r'^$', views.index, name='index'),
    url(r'^keys/$', views.hymn_by_key, name='hymn_by_key'),
    # ex: /hymns/1/
    url(r'^(?P<hymn_id>\d+)/$', views.hymn, name='hymn'),
    url(r'^(?P<hymn_id>\d+)/(?P<hymn_ids>(\d+-)*\d+)/$', views.hymn_list_view, name='hymn_list'),
#    # /musics/score/1/
#    url(r'^score/(?P<score_id>\d+)/$', views.score, name='score'),
#    url(r'^tmp-music/(?P<music_id>\d+)/$', views.tmpMusic, name='tmpMusic'),
#    url(r'^tmp-score/(?P<score_type>\w+)/(?P<score_id>\d+)/$', views.tmpScore, name='tmpScore'),
#    # /musics/weekly-hymns/
    url(r'^weekly-hymns/$', views.weekly_hymns, name='weekly_hymns'),
    url(r'^weekly-hymns/page/(?P<page_num>[\d]+)/$', views.weekly_hymns_page, name='weekly_hymns_page'),
#    url(r'^weekly-hymns-json/$', views.weekly_hymns_json, name='weekly_hymns_json'),
#    url(r'^musics-json/(?P<music_index>\d+)/$', views.musics_json, name='musics_json'),

    # Use the myadmin view
    # url(r'^upload-hymn/$', views.upload_hymn_view, name='upload_hymn_view'),
    # url(r'^edit-hymn/(?P<hymn_id>\d+)/$', views.edit_hymn_view, name='edit_hymn_view'),

    url(r'^edit-weekly-hymn/(?P<weekly_hymn_id>\d+)/$', views.edit_weekly_hymn_view, name='edit_weekly_hymn_view'),
    url(r'^candidates/$', views.candidates_view, name='candidates_view'),
    url(r'^playlist/$', views.playlist_view, name='playlist_view'),
    url(r'^search/$', views.search, name='search'),
    url(r'^(?P<hymn_id>\d+)/saveAudioFile/$', views.save_audio_url, name='saveAudioFile'),
    url(r'^json/random-hymn/$', views.random_hymn_json, name='random_hymn_json'),

    # url(r'^accounts/login/$', views.login_view, name='login_view'),
    # url(r'^accounts/logout/$', views.logout_view, name='logout_view'),
    # url(r'^accounts/register/$', views.register_view, name='register_view'),
#    # for form action to save score file
#    url(r'^saveScoreFile/(?P<upload_type>\w+)/$', views.saveScoreFile, name='saveScoreFile'),
#    url(r'^syncdb/', views.syncdb),#增加URL路径
)

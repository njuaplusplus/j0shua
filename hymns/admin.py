#!/usr/bin/python
# coding=utf-8

from django.contrib import admin
from hymns.models import Hymn_Key, Hymn, Weekly_Hymn

class HymnAdmin(admin.ModelAdmin):
    list_display = ('hymn_index', 'hymn_name', 'hymn_key', 'hymn_isCandidate')
    search_fields = ['hymn_name']

class Weekly_HymnAdmin(admin.ModelAdmin):
    list_display = ('hymn_date', 'hymn_place', 'hymn_order', 'hymn')
    list_filter = ['hymn_date']
    date_hierarchy = 'hymn_date'

# class Candidate_MusicAdmin(admin.ModelAdmin):
#     inlines = [Candidate_Score_No_MusicInline]
#     list_display = ('music_index', 'music_name', 'music_key', 'uploader')
#     search_fields = ['music_name']
# 
# class AudioAdmin(admin.ModelAdmin):
#     list_display = ('music', 'audio_url')

admin.site.register(Hymn, HymnAdmin)
# admin.site.register(Candidate_Music, Candidate_MusicAdmin)
admin.site.register(Weekly_Hymn, Weekly_HymnAdmin)
# admin.site.register(Audio, AudioAdmin)

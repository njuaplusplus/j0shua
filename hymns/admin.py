#!/usr/bin/python
# coding=utf-8

# from django.contrib import admin
# from hymns.models import Hymn_Key, Hymn, Weekly_Hymn, Candidate_Hymn
# 
# class ScoreInline(admin.StackedInline):
#     model = Score
#     extra = 2
# 
# class Candidate_ScoreInline(admin.StackedInline):
#     model = Candidate_Score
#     extra = 2
# 
# class Candidate_Score_No_MusicInline(admin.StackedInline):
#     model = Candidate_Score_No_Music
#     extra = 2
# 
# class MusicAdmin(admin.ModelAdmin):
#     inlines = [ScoreInline, Candidate_ScoreInline]
#     list_display = ('music_index', 'music_name', 'music_key')
#     search_fields = ['music_name']
# 
# class Weekly_HymnAdmin(admin.ModelAdmin):
#     list_display = ('hymn_time', 'hymn_order', 'music')
#     list_filter = ['hymn_time']
#     date_hierarchy = 'hymn_time'
# 
# class Candidate_MusicAdmin(admin.ModelAdmin):
#     inlines = [Candidate_Score_No_MusicInline]
#     list_display = ('music_index', 'music_name', 'music_key', 'uploader')
#     search_fields = ['music_name']
# 
# class AudioAdmin(admin.ModelAdmin):
#     list_display = ('music', 'audio_url')
# 
# admin.site.register(Music, MusicAdmin)
# admin.site.register(Candidate_Music, Candidate_MusicAdmin)
# admin.site.register(Weekly_Hymn, Weekly_HymnAdmin)
# admin.site.register(Audio, AudioAdmin)

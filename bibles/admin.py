#!/usr/bin/python
# coding=utf-8
from django.contrib import admin
from bibles.models import Bible_CHN, Bible_Book_Name, Daily_Verse, Weekly_Verse, Weekly_Reading, Weekly_Recitation

# Register your models here.
# class Bible_NIVAdmin(admin.ModelAdmin):
#     list_display = ('book', 'chapternum', 'versenum', 'verse')

class Bible_CHNAdmin(admin.ModelAdmin):
    list_display = ('book', 'chapternum', 'versenum', 'verse')

class Bible_Book_NameAdmin(admin.ModelAdmin):
    list_display = ('book_name_zh', 'book_name_en', 'chapternums')

class Daily_VerseAdmin(admin.ModelAdmin):
    list_display = ('verse_date', 'start_verse', 'end_verse')

#admin.site.register(Bible_NIV, Bible_NIVAdmin)
admin.site.register(Bible_CHN, Bible_CHNAdmin)
admin.site.register(Bible_Book_Name, Bible_Book_NameAdmin)
admin.site.register(Daily_Verse, Daily_VerseAdmin)
admin.site.register(Weekly_Verse)
admin.site.register(Weekly_Reading)
admin.site.register(Weekly_Recitation)

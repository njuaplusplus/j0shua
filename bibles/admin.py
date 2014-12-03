#!/usr/bin/python
# coding=utf-8
from django.contrib import admin
from bibles.models import Bible_CHN, Bible_Book_Name

# Register your models here.
# class Bible_NIVAdmin(admin.ModelAdmin):
#     list_display = ('book', 'chapternum', 'versenum', 'verse')

class Bible_CHNAdmin(admin.ModelAdmin):
    list_display = ('book', 'chapternum', 'versenum', 'verse')

class Bible_Book_NameAdmin(admin.ModelAdmin):
    list_display = ('book_name_zh', 'book_name_en', 'chapternums')

#admin.site.register(Bible_NIV, Bible_NIVAdmin)
admin.site.register(Bible_CHN, Bible_CHNAdmin)
admin.site.register(Bible_Book_Name, Bible_Book_NameAdmin)

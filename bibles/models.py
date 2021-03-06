#!/usr/local/bin/python
# coding=utf-8
from django.db import models

# Create your models here.
# class Bible_NIV(models.Model):
#     versenum = models.IntegerField(u'节')
#     chapternum = models.IntegerField(u'章')
#     book = models.CharField(u'卷', max_length=30)
#     verse = models.TextField(u'经文')
#     def __str__(self):
#         return "%s:%s:%s" % (self.book, self.chapternum, self.versenum)

class Bible_Book_Name(models.Model):
    ''' The chinese book name with the corresponding English name
    '''
    book_name_zh = models.CharField('中文名', max_length=30)
    book_name_en = models.CharField('英文名', max_length=30)
    chapternums = models.IntegerField('章节数', default=0)
    def __str__(self):
        return "%s(%s)" % (self.book_name_zh, self.book_name_en)

class Bible_CHN(models.Model):
    versenum = models.IntegerField('节')
    chapternum = models.IntegerField('章')
    book = models.ForeignKey(Bible_Book_Name, verbose_name='卷')
    verse = models.TextField('经文')
    def __str__(self):
        return "%s %s:%s" % (self.book, self.chapternum, self.versenum)

class Bible_NIV2011(models.Model):
    versenum = models.IntegerField('节')
    chapternum = models.IntegerField('章')
    book = models.ForeignKey(Bible_Book_Name, verbose_name='卷')
    verse = models.TextField('经文')
    def __str__(self):
        return "%s %s:%s" % (self.book, self.chapternum, self.versenum)

class Daily_Verse(models.Model):
    verse_date = models.DateField('日期')
    start_verse = models.ForeignKey(Bible_CHN, verbose_name='起始经文', related_name='daily_start_verse_set')
    end_verse = models.ForeignKey(Bible_CHN, verbose_name='结束经文', related_name='daily_end_verse_set')
    def __str__(self):
        return "%s:%s-%s" % (self.verse_date, self.start_verse, self.end_verse)

class Weekly_Verse(models.Model):
    verse_date = models.DateField('日期')
    start_verse = models.ForeignKey(Bible_CHN, verbose_name='起始经文', related_name='weekly_start_verse_set')
    end_verse = models.ForeignKey(Bible_CHN, verbose_name='结束经文', related_name='weekly_end_verse_set')
    def __str__(self):
        return "%s:%s-%s" % (self.verse_date, self.start_verse, self.end_verse)

class Weekly_Reading(models.Model):
    ''' 每周读经
    '''
    verse_date = models.DateField('日期')
    start_verse = models.ForeignKey(Bible_CHN, verbose_name='起始经文', related_name='weekly_reading_start_verse_set')
    end_verse = models.ForeignKey(Bible_CHN, verbose_name='结束经文', related_name='weekly_reading_end_verse_set')
    def __str__(self):
        return "%s:%s-%s" % (self.verse_date, self.start_verse, self.end_verse)

class Weekly_Recitation(models.Model):
    ''' 每周背经
    '''
    verse_date = models.DateField('日期')
    start_verse = models.ForeignKey(Bible_CHN, verbose_name='起始经文', related_name='weekly_recitation_start_verse_set')
    end_verse = models.ForeignKey(Bible_CHN, verbose_name='结束经文', related_name='weekly_recitation_end_verse_set')
    def __str__(self):
        return "%s:%s-%s" % (self.verse_date, self.start_verse, self.end_verse)

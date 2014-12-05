#!/usr/local/bin/python
# coding=utf-8
from django.db import models

# Create your models here.
# class Bible_NIV(models.Model):
#     versenum = models.IntegerField(u'节')
#     chapternum = models.IntegerField(u'章')
#     book = models.CharField(u'卷', max_length=30)
#     verse = models.TextField(u'经文')
#     def __unicode__(self):
#         return "%s:%s:%s" % (self.book, self.chapternum, self.versenum)

class Bible_Book_Name(models.Model):
    ''' The chinese book name with the corresponding English name
    '''
    book_name_zh = models.CharField(u'中文名', max_length=30)
    book_name_en = models.CharField(u'英文名', max_length=30)
    chapternums = models.IntegerField(u'章节数', default=0)
    def __unicode__(self):
        return u"%s %s" % (self.book_name_zh, self.book_name_en)

class Bible_CHN(models.Model):
    versenum = models.IntegerField(u'节')
    chapternum = models.IntegerField(u'章')
    book = models.ForeignKey(Bible_Book_Name, verbose_name=u'卷')
    verse = models.TextField(u'经文')
    def __unicode__(self):
        return u"%s:%s:%s" % (self.book, self.chapternum, self.versenum)

class Daily_Verse(models.Model):
    verse_date = models.DateField(u'日期')
    start_verse = models.ForeignKey(Bible_CHN, verbose_name=u'起始经文', related_name='daily_start_verse_set')
    end_verse = models.ForeignKey(Bible_CHN, verbose_name=u'结束经文', related_name='daily_end_verse_set')
    def __unicode__(self):
        return u"%s:%s-%s" % (self.verse_date, self.start_verse, self.end_verse)

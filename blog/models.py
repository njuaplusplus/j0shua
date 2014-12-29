#!/usr/local/bin/python
# coding=utf-8

from django.db import models
from django.utils.translation import ugettext as _
from markdown import markdown
from django.contrib.auth.models import User
from uuslug import uuslug

class Category(models.Model) :
    """Category Model"""
    title = models.CharField(
        verbose_name = _(u'名称'),
        help_text = _(u' '),
        max_length = 255
    )
    slug = models.SlugField(
        verbose_name = _(u'Slug'),
        help_text = _(u'Uri identifier.'),
        max_length = 255,
        unique = True
    )

    class Meta:
        app_label = _(u'blog')
        verbose_name = _(u"Category")
        verbose_name_plural = _(u"Categories")
        ordering = ['title',]

    def save(self, *args, **kwargs):
        self.slug = uuslug(self.title, instance=self, max_length=32, word_boundary=True)
        super(Category, self).save(*args, **kwargs)

    def __unicode__(self):
        return "%s" % (self.title,)

class Article(models.Model) :
    """Article Model"""
    title = models.CharField(
        verbose_name = _(u'标题'),
        help_text = _(u' '),
        max_length = 255
    )
    slug = models.SlugField(
        verbose_name = _(u'Slug'),
        help_text = _(u'Uri identifier.'),
        max_length = 255,
        unique = True
    )
    cover = models.ImageField(
        verbose_name = _(u'封面'),
        help_text = _(u'若留空, 则使用默认图片'),
        upload_to='blogs/images/%Y/%m/%d',
        null = True,
        blank = True
    )
    excerpt = models.TextField(
        verbose_name = _(u'摘要'),
        help_text = _(u' '),
        null = True,
        blank = True
    )

    author = models.ForeignKey(User, verbose_name=_(u'作者'))
    content_markdown = models.TextField(
        verbose_name = _(u'内容 (Markdown)'),
        help_text = _(u' '),
    )
    content_markup = models.TextField(
        verbose_name = _(u'内容 (Markup)'),
        help_text = _(u' '),
    )
    categories = models.ManyToManyField(
        Category,
        verbose_name = _(u'分类'),
        help_text = _(u' '),
        null = True,
        blank = True
    )
    date_publish = models.DateTimeField(
        verbose_name = _(u'发布日期'),
        help_text = _(u' ')
    )

    class Meta:
        app_label = _(u'blog')
        verbose_name = _(u"Article")
        verbose_name_plural = _(u"Articles")
        ordering = ['-date_publish']

    def save(self, *args, **kwargs):
        self.slug = uuslug(self.title, instance=self, max_length=32, word_boundary=True)
        self.content_markup = markdown(self.content_markdown, ['codehilite', 'attr_list'])
        super(Article, self).save(*args, **kwargs)

    def __unicode__(self):
        return "%s" % (self.title,)

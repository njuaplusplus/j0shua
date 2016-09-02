#!/usr/local/bin/python
# coding=utf-8

from django.db import models
from django.utils.translation import ugettext as _
from markdown import markdown
from django.contrib.auth.models import User
from uuslug import uuslug
from django import forms
from pagedown.widgets import PagedownWidget
# from bootstrap3_datetime.widgets import DateTimePicker
from datetimewidget.widgets import DateTimeWidget

class Category(models.Model) :
    """Category Model"""
    title = models.CharField(
        verbose_name = _('名称'),
        help_text = _(' '),
        max_length = 255
    )
    slug = models.SlugField(
        verbose_name = _('Slug'),
        help_text = _('Uri identifier.'),
        max_length = 255,
        unique = True
    )

    class Meta:
        app_label = _('blog')
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ['title',]

    def save(self, *args, **kwargs):
        if not self.slug.strip():
            # slug is null or empty
            self.slug = uuslug(self.title, instance=self, max_length=32, word_boundary=True)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return "%s" % (self.title,)

class Article(models.Model) :
    """Article Model"""
    title = models.CharField(
        verbose_name = _('标题'),
        help_text = _(' '),
        max_length = 255
    )
    slug = models.SlugField(
        verbose_name = _('固定链接'),
        help_text = _('本文章的短网址(Uri identifier).'),
        max_length = 255,
        unique = True
    )
    cover = models.ImageField(
        verbose_name = _('封面'),
        help_text = _('若留空, 则使用默认图片'),
        upload_to='blogs/images/%Y/%m/%d',
        null = True,
        blank = True
    )
    excerpt = models.TextField(
        verbose_name = _('摘要'),
        help_text = _(' '),
        null = True,
        blank = True
    )

    author = models.ForeignKey(User, verbose_name=_('作者'))
    content_markdown = models.TextField(
        verbose_name = _('内容 (Markdown)'),
        help_text = _(' '),
    )
    content_markup = models.TextField(
        verbose_name = _('内容 (Markup)'),
        help_text = _(' '),
    )
    categories = models.ManyToManyField(
        Category,
        verbose_name = _('分类'),
        help_text = _(' '),
        blank = True
    )
    date_publish = models.DateTimeField(
        verbose_name = _('发布日期'),
        help_text = _(' ')
    )
    is_approved = models.BooleanField(
        verbose_name = _('通过审核'),
        default = False
    )

    class Meta:
        app_label = _('blog')
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")
        ordering = ['-date_publish']

    def save(self, *args, **kwargs):
        if not self.slug.strip():
            # slug is null or empty
            self.slug = uuslug(self.title, instance=self, max_length=32, word_boundary=True)
        if self.is_approved is None:
            self.is_approved = False
        self.content_markup = markdown(self.content_markdown, ['codehilite', 'attr_list'])
        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return "%s" % (self.title,)

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        dateTimeOptions = {
            'todayBtn' : 'true',
        }
        widgets = {
            'content_markdown' : PagedownWidget(),
            # 'date_publish' : DateTimePicker(options={"format": "YYYY-MM-DD HH:mm", "pickSeconds": False, "language": 'zh-cn', }),
            'date_publish' : DateTimeWidget(usel10n=True, bootstrap_version=3, options = dateTimeOptions),
            'title' : forms.TextInput(attrs={'class':'form-control'}),
            'slug' : forms.TextInput(attrs={'class':'form-control'}),
            'excerpt' : forms.Textarea(attrs={'class':'form-control'}),
            'categories' : forms.SelectMultiple(attrs={'class':'form-control'}),
        }
        exclude = ['content_markup', 'author', 'is_approved', ]


#!/usr/bin/python
# coding=utf-8

from django.db import models
from django.utils.translation import ugettext as _


class Contact(models.Model):
    """
    Model for contact us
    """
    name = models.CharField(
        verbose_name=_(u'姓名'),
        max_length=255
    )
    email = models.EmailField(
        verbose_name=_(u'邮件')
    )
    phone = models.CharField(
        verbose_name=_(u'电话'),
        max_length=255
    )
    message = models.TextField(
        verbose_name=_(u'信息')
    )
    date_created = models.DateTimeField(
        verbose_name=_(u'留言日期')
    )

    def __unicode__(self):
        return u'%s %s' % (self.name, self.email,)

    class Meta:
        app_label = _(u'gospel')
        verbose_name = _(u"Contact")
        verbose_name_plural = _(u"Contacts")
        ordering = ['-date_created']

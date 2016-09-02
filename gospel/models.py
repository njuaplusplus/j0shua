#!/usr/bin/python
# coding=utf-8

from django.db import models
from django.utils.translation import ugettext as _


class Contact(models.Model):
    """
    Model for contact us
    """
    name = models.CharField(
        verbose_name=_('姓名'),
        max_length=255
    )
    email = models.EmailField(
        verbose_name=_('邮件')
    )
    phone = models.CharField(
        verbose_name=_('电话'),
        max_length=255
    )
    message = models.TextField(
        verbose_name=_('信息')
    )
    date_created = models.DateTimeField(
        verbose_name=_('留言日期')
    )

    def __str__(self):
        return '%s %s' % (self.name, self.email,)

    class Meta:
        app_label = _('gospel')
        verbose_name = _("Contact")
        verbose_name_plural = _("Contacts")
        ordering = ['-date_created']

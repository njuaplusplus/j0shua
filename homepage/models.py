#!/usr/local/bin/python
# coding=utf-8
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class User_Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    duoshuo_id = models.IntegerField(default=0)
    token = models.IntegerField(default=0)
    avatar = models.URLField(blank=True, null=True)

    def __unicode__(self):
        return self.user.username

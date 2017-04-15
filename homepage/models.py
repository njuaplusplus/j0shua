#!/usr/local/bin/python
# coding=utf-8
from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext as _


class User_Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    duoshuo_id = models.IntegerField(default=0)
    token = models.IntegerField(default=0)
    avatar = models.URLField(blank=True, null=True)
    unionid = models.CharField(
        help_text=_('同一用户，对同一个微信开放平台下的不同应用，unionid是相同的'),
        max_length=255
    )
    openid = models.CharField(
        help_text=_('开发者可通过OpenID来获取用户基本信息'),
        max_length=255
    )

    def __str__(self):
        return self.user.username


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [ 'first_name', 'last_name', 'email']
        widgets = {
            'first_name' : forms.TextInput(attrs={'class':'form-control'}),
            'last_name' : forms.TextInput(attrs={'class':'form-control'}),
            'email' : forms.EmailInput(attrs={'class':'form-control'}),
        }

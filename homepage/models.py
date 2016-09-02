#!/usr/local/bin/python
# coding=utf-8
from django.db import models
from django.contrib.auth.models import User
from django import forms

# Create your models here.

class User_Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    duoshuo_id = models.IntegerField(default=0)
    token = models.IntegerField(default=0)
    avatar = models.URLField(blank=True, null=True)

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

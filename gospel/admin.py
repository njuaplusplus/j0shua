#!/usr/bin/python
# coding=utf-8

from django.contrib import admin
from .models import Contact


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'date_created', 'message',)
    search_fields = ('name',)

admin.site.register(Contact, ContactAdmin)

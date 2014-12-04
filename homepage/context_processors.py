#!/usr/local/bin/python
# coding=utf-8

def analytics_code(request):
    from django.conf import settings
    return {'analytics_code' : settings.ANALYTICS_CODE}

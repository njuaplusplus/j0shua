#!/usr/local/bin/python
# coding=utf-8
from django.shortcuts import render

# Create your views here.

def docs_view(request, doc_name):
    tmplate = 'docs/%s.html' % (doc_name)
    return render(request, tmplate)

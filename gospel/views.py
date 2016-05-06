#!/usr/bin/python
# coding=utf-8

from django.shortcuts import render
from django.http import HttpResponse
from .models import Contact
from django.utils import timezone


# Create your views here.
def index(request):
    if request.method == 'GET':
        return render(request, 'gospel/index.html')


def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name', 'no name')
        email = request.POST.get('email', 'no email')
        phone = request.POST.get('phone', 'no phone')
        message = request.POST.get('message', 'no message')
        print name, email, phone, message
        Contact.objects.create(name=name, email=email,
                               phone=phone, message=message,
                               date_created=timezone.now())
        return HttpResponse('Success!')

    return HttpResponse('HeHe!')

#!/usr/local/bin/python
# coding=utf-8
# Create your views here.

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib import auth
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse

from bibles.models import Bible_CHN, Bible_Book_Name, Daily_Verse

import json

def index(request):
    daily_verse = Daily_Verse.objects.order_by('-verse_date').first()
    verses = None
    if daily_verse:
        # Get the daily verses
        verses = Bible_CHN.objects.filter(pk__range=(daily_verse.start_verse.id, daily_verse.end_verse.id)).order_by('pk')
    context = {'verses' : list(verses)}
    return render(request, 'bibles/index.html', context)

def bible(request):
    books = Bible_Book_Name.objects.all()
    # cur_book is used to record the book that the user read last time
    # chapternum is used to record the chapter that the user read last time
    cur_book = books[0]
    cur_chapternum = 1
    # First, try to get from the get params
    try:
        cur_book_id = int(request.GET.get('bookid', ''))
        cur_chapternum = int(request.GET.get('chapternum', ''))
    except ValueError:
        cur_chapternum = 1
    else:
        cur_book = books.get(pk=cur_book_id)
    verses = cur_book.bible_chn_set.filter(chapternum=cur_chapternum).order_by('versenum')
    context = {'verses': verses, 'books': books, 'cur_book_id': cur_book.id, 'cur_chapternum': cur_chapternum, 'chapternums': xrange(cur_book.chapternums)}
    return render(request, 'bibles/bible.html', context)

def json_bible(request, book_id, chapternum):
    response_json = []
    book = None
    try:
        book = Bible_Book_Name.objects.get(pk=book_id)
    except Bible_Book_Name.DoesNotExist:
        return HttpResponse(json.dumps([]), content_type="application/json")
    else:
        verses = book.bible_chn_set.filter(chapternum=chapternum).order_by('versenum')
        response_json = [(v.versenum, v.verse) for v in verses]
        return HttpResponse(json.dumps(response_json), content_type="application/json")

def login_view(request):
    if request.user is not None and request.user.is_active:
        return HttpResponseRedirect(reverse('bibles:index'))
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    next_url = request.POST.get('next', '')
    if len(next_url) ==  0:
        next_url = request.GET.get('next', '')
        if len(next_url) == 0:
            next_url = reverse('bibles:index')
    if next_url == reverse('bibles:login_view'):
        next_url = reverse('bibles:index')
    if user is not None and user.is_active:
        # Correct password, and the user is marked 'active'
        auth.login(request, user)
        # Redirect to a success page.
        return HttpResponseRedirect(next_url)
    else:
        # Show an error page
        return render(request, 'bibles/login.html', {'next': next_url})

def logout_view(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('bibles:login_view'));

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect(reverse('bibles:logout_view'))
    else:
        form = UserCreationForm()
    return render(request, 'bibles/register.html', { 'form': form, })

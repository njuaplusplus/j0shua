#!/usr/local/bin/python
# coding=utf-8
# Create your views here.

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib import auth
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse
# from django.utils import timezone
import datetime

from bibles.models import Bible_CHN, Bible_Book_Name, Daily_Verse, Weekly_Verse, Weekly_Reading, Weekly_Recitation, Bible_NIV2011

import json

def index(request):
    today = datetime.date.today()
    coming_sunday = today + datetime.timedelta(days=6-today.weekday())
    past_monday = today - datetime.timedelta(days=today.weekday())
    daily_verse = Daily_Verse.objects.filter(verse_date=today).first()
    weekly_verse = Weekly_Verse.objects.filter(verse_date=coming_sunday).first()
    weekly_readings = list(Weekly_Reading.objects.filter(verse_date__range=(past_monday,coming_sunday)).order_by('-verse_date'))
    weekly_recitations = []
    if weekly_readings:
        latest_date = max([w.verse_date for w in weekly_readings])
        weekly_readings = [w for w in weekly_readings if w.verse_date==latest_date]
        weekly_recitations = Weekly_Recitation.objects.filter(verse_date=latest_date).order_by('-pk')
    daily_verses = []
    weekly_verses = []
    weekly_recitation_verses = []
    if daily_verse:
        # Get the daily verses
        daily_verses = Bible_CHN.objects.filter(pk__range=(daily_verse.start_verse.id, daily_verse.end_verse.id)).order_by('pk')
    if weekly_verse:
        # Get the weekly verses
        weekly_verses = Bible_CHN.objects.filter(pk__range=(weekly_verse.start_verse.id, weekly_verse.end_verse.id)).order_by('pk')
    for wr in weekly_recitations:
        weekly_recitation_verses.append((wr, Bible_CHN.objects.filter(pk__range=(wr.start_verse.id,wr.end_verse.id)).order_by('pk')))
    context = {'daily_verses' : list(daily_verses), 'weekly_verses': list(weekly_verses), 'weekly_readings': weekly_readings, 'weekly_recitation_verses': weekly_recitation_verses,}
    return render(request, 'bibles/index.html', context)

def bible(request):
    return bible_version(request, 'chn')

def bible_version(request, version):
    books = Bible_Book_Name.objects.all()
    # cur_book is used to record the book that the user read last time
    # chapternum is used to record the chapter that the user read last time
    cur_book = books[0]
    cur_chapternum = 1
    highlight_verses = []
    cur_start_verse_id = 0
    cur_end_verse_id = 0
    # First, try to get from the get params
    try:
        cur_book_id = int(request.GET.get('bookid', ''))
        cur_chapternum = int(request.GET.get('chapternum', ''))
        cur_start_verse_id, cur_end_verse_id = [int(x) for x in request.GET.get('verses','-').split('-')]
    except ValueError:
        cur_chapternum = 1
    else:
        cur_book = books.get(pk=cur_book_id)
        if cur_start_verse_id and cur_end_verse_id:
            print cur_start_verse_id, cur_end_verse_id
            highlight_verses.extend(xrange(cur_start_verse_id, cur_end_verse_id+1))
    if version == 'niv':
        verses = cur_book.bible_niv2011_set.filter(chapternum=cur_chapternum).order_by('versenum')
    else:
        verses = cur_book.bible_chn_set.filter(chapternum=cur_chapternum).order_by('versenum')
    print highlight_verses
    context = {
        'verses': verses,
        'books': books,
        'cur_book_id': cur_book.id,
        'cur_chapternum': cur_chapternum,
        'chapternums': xrange(1, cur_book.chapternums+1),
        'highlight_verses': highlight_verses,
        'version': version,
    }
    return render(request, 'bibles/bible.html', context)

def json_bible(request, version, book_id, chapternum):
    response_json = []
    book = None
    try:
        book = Bible_Book_Name.objects.get(pk=book_id)
    except Bible_Book_Name.DoesNotExist:
        return HttpResponse(json.dumps([]), content_type="application/json")
    else:
        if version == 'niv':
            verses = book.bible_niv2011_set.filter(chapternum=chapternum).order_by('versenum')
        else:
            verses = book.bible_chn_set.filter(chapternum=chapternum).order_by('versenum')
        response_json = [(v.versenum, v.verse) for v in verses]
        return HttpResponse(json.dumps(response_json), content_type="application/json")

# Use homepage login
# def login_view(request):
#     if request.user is not None and request.user.is_active:
#         return HttpResponseRedirect(reverse('bibles:index'))
#     username = request.POST.get('username', '')
#     password = request.POST.get('password', '')
#     user = auth.authenticate(username=username, password=password)
#     next_url = request.POST.get('next', '')
#     if len(next_url) ==  0:
#         next_url = request.GET.get('next', '')
#         if len(next_url) == 0:
#             next_url = reverse('bibles:index')
#     if next_url == reverse('bibles:login_view'):
#         next_url = reverse('bibles:index')
#     if user is not None and user.is_active:
#         # Correct password, and the user is marked 'active'
#         auth.login(request, user)
#         # Redirect to a success page.
#         return HttpResponseRedirect(next_url)
#     else:
#         # Show an error page
#         return render(request, 'bibles/login.html', {'next': next_url})
# 
# def logout_view(request):
#     auth.logout(request)
#     return HttpResponseRedirect(reverse('bibles:login_view'));
# 
# def register_view(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             new_user = form.save()
#             return HttpResponseRedirect(reverse('bibles:logout_view'))
#     else:
#         form = UserCreationForm()
#     return render(request, 'bibles/register.html', { 'form': form, })

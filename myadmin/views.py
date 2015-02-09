#!/usr/local/bin/python
# coding=utf-8
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import auth
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from hymns.models import Weekly_Hymn, Hymn, Worship_Location, Hymn_Form
from bibles.models import Daily_Verse, Weekly_Verse, Bible_Book_Name, Weekly_Reading, Weekly_Recitation
from blog.models import Article, ArticleForm
from homepage.models import UserProfileForm

import datetime
import re
# Create your views here.

@login_required(login_url='/myadmin/accounts/login/')
def index(request):
    return render(request, 'myadmin/index.html')

@login_required(login_url='/myadmin/accounts/login/')
def users_view(request):
    if not request.user.groups.filter(name='admins'):
        return render(request, 'hymns/test_result.html', {'result': '权限不够', })
    users = User.objects.filter(is_superuser=False)
    return render(request, 'myadmin/users.html', {'users': users})

@login_required(login_url='/myadmin/accounts/login/')
def weekly_hymns_view(request):
    if not request.user.groups.filter(name='admins'):
        return render(request, 'hymns/test_result.html', {'result': '权限不够', })
    if request.method == 'POST':
        datestr = request.POST.get('hymn-date', '').split('-')
        hymn_places = request.POST.getlist('hymn-place', '')
        hymn_orders = request.POST.getlist('hymn-order', '')
        weekly_hymns = request.POST.getlist('weekly-hymn', '')
        print 'hymn-date: ' , datestr
        print 'hymn_places: ' , hymn_places
        print 'hymn_orders: ' , hymn_orders
        print 'weekly_hymns: ' , weekly_hymns
        hymn_date = datetime.date(int(datestr[0]), int(datestr[1]), int(datestr[2]))
        for i in xrange(len(hymn_places)):
            hymn_place = Worship_Location.objects.get(pk=hymn_places[i])
            hymn = Hymn.objects.get(pk=weekly_hymns[i])
            weekly_hymn = Weekly_Hymn.objects.get_or_create(hymn_date=hymn_date, hymn_order=hymn_orders[i], hymn_place=hymn_place, hymn=hymn)

        return HttpResponseRedirect(reverse('myadmin:weekly_hymns_view'))
    else:
        weekly_hymns = Weekly_Hymn.objects.order_by('-hymn_date', 'hymn_place', 'hymn_order')
        all_hymns = Hymn.objects.all()
        context = {'weekly_hymns': weekly_hymns, 'all_hymns': all_hymns}
        return render(request, 'myadmin/weekly_hymns.html', context)

@login_required(login_url='/myadmin/accounts/login/')
def daily_verses_view(request):
    if not request.user.groups.filter(name='admins'):
        return render(request, 'hymns/test_result.html', {'result': '权限不够', })
    if request.method == 'POST':
        datestr = request.POST.get('verse-date', '').split('-')
        try:
            start_verse_book_id = int(request.POST.get('start-verse-book', ''))
            start_verse_chapternum = int(request.POST.get('start-verse-chapternum', ''))
            start_verse_versenum = int(request.POST.get('start-verse-versenum', ''))
            end_verse_book_id = int(request.POST.get('end-verse-book', ''))
            end_verse_chapternum = int(request.POST.get('end-verse-chapternum', ''))
            end_verse_versenum = int(request.POST.get('end-verse-versenum', ''))
        except ValueError:
            return render(request, 'hymns/test_result.html', {'result': '格式错误', })
        else:
            verse_date = datetime.date(int(datestr[0]), int(datestr[1]), int(datestr[2]))
            start_verse_book = Bible_Book_Name.objects.get(pk=start_verse_book_id)
            start_verse = start_verse_book.bible_chn_set.get(chapternum=start_verse_chapternum, versenum=start_verse_versenum)
            end_verse_book = Bible_Book_Name.objects.get(pk=end_verse_book_id)
            end_verse = end_verse_book.bible_chn_set.get(chapternum=end_verse_chapternum, versenum=end_verse_versenum)
            Daily_Verse(verse_date=verse_date,start_verse=start_verse,end_verse=end_verse).save()
        return HttpResponseRedirect(reverse('myadmin:daily_verses_view'))
    else:
        daily_verses = Daily_Verse.objects.order_by('-verse_date')
        books = Bible_Book_Name.objects.all()
        today_verse_exists = daily_verses and daily_verses.first().verse_date == datetime.date.today()
        context = {'books': books, 'daily_verses': daily_verses, 'today_verse_exists': today_verse_exists,}
        return render(request, 'myadmin/daily_verses.html', context)

@login_required(login_url='/myadmin/accounts/login/')
def weekly_verses_view(request):
    if not request.user.groups.filter(name='admins'):
        return render(request, 'hymns/test_result.html', {'result': '权限不够', })
    if request.method == 'POST':
        datestr = request.POST.get('verse-date', '').split('-')
        try:
            start_verse_book_id = int(request.POST.get('start-verse-book', ''))
            start_verse_chapternum = int(request.POST.get('start-verse-chapternum', ''))
            start_verse_versenum = int(request.POST.get('start-verse-versenum', ''))
            end_verse_book_id = int(request.POST.get('end-verse-book', ''))
            end_verse_chapternum = int(request.POST.get('end-verse-chapternum', ''))
            end_verse_versenum = int(request.POST.get('end-verse-versenum', ''))
        except ValueError:
            return render(request, 'hymns/test_result.html', {'result': '格式错误', })
        else:
            verse_date = datetime.date(int(datestr[0]), int(datestr[1]), int(datestr[2]))
            start_verse_book = Bible_Book_Name.objects.get(pk=start_verse_book_id)
            start_verse = start_verse_book.bible_chn_set.get(chapternum=start_verse_chapternum, versenum=start_verse_versenum)
            end_verse_book = Bible_Book_Name.objects.get(pk=end_verse_book_id)
            end_verse = end_verse_book.bible_chn_set.get(chapternum=end_verse_chapternum, versenum=end_verse_versenum)
            Weekly_Verse(verse_date=verse_date,start_verse=start_verse,end_verse=end_verse).save()
        return HttpResponseRedirect(reverse('myadmin:weekly_verses_view'))
    else:
        weekly_verses = Weekly_Verse.objects.order_by('-verse_date')
        books = Bible_Book_Name.objects.all()
        today = datetime.date.today()
        coming_sunday = today + datetime.timedelta(days=6-today.weekday())
        weekly_verse_exists = weekly_verses and weekly_verses.first().verse_date == coming_sunday
        context = {'books': books, 'weekly_verses': weekly_verses, 'weekly_verse_exists': weekly_verse_exists,}
        return render(request, 'myadmin/weekly_verses.html', context)

@login_required(login_url='/myadmin/accounts/login/')
def weekly_readings_view(request):
    if not request.user.groups.filter(name='admins'):
        return render(request, 'hymns/test_result.html', {'result': '权限不够', })
    if request.method == 'POST':
        datestr = request.POST.get('verse-date', '').split('-')
        try:
            start_verse_book_id = int(request.POST.get('start-verse-book', ''))
            start_verse_chapternum = int(request.POST.get('start-verse-chapternum', ''))
            end_verse_book_id = int(request.POST.get('end-verse-book', ''))
            end_verse_chapternum = int(request.POST.get('end-verse-chapternum', ''))
        except ValueError:
            return render(request, 'hymns/test_result.html', {'result': '格式错误', })
        else:
            start_verse_versenum = 1
            end_verse_versenum = 1
            verse_date = datetime.date(int(datestr[0]), int(datestr[1]), int(datestr[2]))
            start_verse_book = Bible_Book_Name.objects.get(pk=start_verse_book_id)
            start_verse = start_verse_book.bible_chn_set.get(chapternum=start_verse_chapternum, versenum=start_verse_versenum)
            end_verse_book = Bible_Book_Name.objects.get(pk=end_verse_book_id)
            end_verse = end_verse_book.bible_chn_set.get(chapternum=end_verse_chapternum, versenum=end_verse_versenum)
            Weekly_Reading(verse_date=verse_date,start_verse=start_verse,end_verse=end_verse).save()
        return HttpResponseRedirect(reverse('myadmin:weekly_readings_view'))
    else:
        weekly_readings = Weekly_Reading.objects.order_by('-verse_date')
        books = Bible_Book_Name.objects.all()
        context = {'books': books, 'weekly_readings': weekly_readings,}
        return render(request, 'myadmin/weekly_readings.html', context)

@login_required(login_url='/myadmin/accounts/login/')
def weekly_recitations_view(request):
    if not request.user.groups.filter(name='admins'):
        return render(request, 'hymns/test_result.html', {'result': '权限不够', })
    if request.method == 'POST':
        datestr = request.POST.get('verse-date', '').split('-')
        try:
            start_verse_book_id = int(request.POST.get('start-verse-book', ''))
            start_verse_chapternum = int(request.POST.get('start-verse-chapternum', ''))
            start_verse_versenum = int(request.POST.get('start-verse-versenum', ''))
            end_verse_book_id = int(request.POST.get('end-verse-book', ''))
            end_verse_chapternum = int(request.POST.get('end-verse-chapternum', ''))
            end_verse_versenum = int(request.POST.get('end-verse-versenum', ''))
        except ValueError:
            return render(request, 'hymns/test_result.html', {'result': '格式错误', })
        else:
            verse_date = datetime.date(int(datestr[0]), int(datestr[1]), int(datestr[2]))
            start_verse_book = Bible_Book_Name.objects.get(pk=start_verse_book_id)
            start_verse = start_verse_book.bible_chn_set.get(chapternum=start_verse_chapternum, versenum=start_verse_versenum)
            end_verse_book = Bible_Book_Name.objects.get(pk=end_verse_book_id)
            end_verse = end_verse_book.bible_chn_set.get(chapternum=end_verse_chapternum, versenum=end_verse_versenum)
            Weekly_Recitation(verse_date=verse_date,start_verse=start_verse,end_verse=end_verse).save()
        return HttpResponseRedirect(reverse('myadmin:weekly_recitations_view'))
    else:
        weekly_recitations = Weekly_Recitation.objects.order_by('-verse_date')
        books = Bible_Book_Name.objects.all()
        context = {'books': books, 'weekly_recitations': weekly_recitations,}
        return render(request, 'myadmin/weekly_recitations.html', context)

@login_required(login_url='/myadmin/accounts/login/')
def write_post_view(request):
    if not request.user.groups.filter(name='admins'):
        return render(request, 'hymns/test_result.html', {'result': '权限不够', })
    if request.method == 'POST':
        article_form = ArticleForm(request.POST, request.FILES)
        if article_form.is_valid():
            article = article_form.save(commit=False)
            article.author = request.user
            article.save()
            article_form.save_m2m()
            return HttpResponseRedirect(reverse('blog:single_post', args=(article.slug,)))
    else:
        article_form = ArticleForm()
    return render(request, 'myadmin/write_post.html', {'article_form': article_form, })

@login_required(login_url='/myadmin/accounts/login/')
def edit_post_view(request, post_id):
    article = get_object_or_404(Article, pk=post_id)
    if not request.user.groups.filter(name='admins') and request.user != article.author:
        return render(request, 'hymns/test_result.html', {'result': '权限不够', })
    if request.method == 'POST':
        article_form = ArticleForm(request.POST, request.FILES, instance=article)
        if article_form.is_valid():
            article_form.save()
            return HttpResponseRedirect(reverse('blog:single_post', args=(article.slug,)))
    else:
        article_form = ArticleForm(instance=article)
    return render(request, 'myadmin/write_post.html', {'article_form': article_form, })

@login_required(login_url='/myadmin/accounts/login/')
def user_profile_view(request):
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            return HttpResponseRedirect(reverse('myadmin:user_profile_view'))
    else:
        profile_form = UserProfileForm(instance=request.user)
    return render(request, 'myadmin/user_profile.html', {'profile_form': profile_form, })

@login_required(login_url='/myadmin/accounts/login/')
def upload_hymn_view(request):
    ''' Upload the hymn

    '''
    if not request.user.groups.filter(name='uploaders') and not request.user.has_perm(u'hymns.add_hymn') and not request.user.groups.filter(name='admins'):
        return render(request, 'hymns/test_result.html', {'result': '权限不够', })
    if request.method == 'POST':
        form = Hymn_Form(request.POST, request.FILES)
        if form.is_valid():
            hymn = form.save(commit=False)
            if hymn.hymn_audio:
                tmp = re.findall('zanmeishi.com/song/(\d+)\.html',hymn.hymn_audio)
                if len(tmp) == 1:
                    audio_id = tmp[0]
                    hymn.hymn_audio = "http://api.zanmeishi.com/song/p/%s.mp3" % audio_id
                else:
                    return render(request, 'hymns/test_result.html', {'result': '链接地址不对', })
            hymn.hymn_isCandidate = True
            hymn.hymn_uploader = request.user
            hymn.save()
            form.save_m2m()
            print 'Hymn saved! %s' % hymn.id
            return HttpResponseRedirect(reverse('hymns:hymn', args=(hymn.id,)))
    else:
        form = Hymn_Form()
    return render(request, 'myadmin/upload_hymn.html', {'hymn_form': form, })

@login_required(login_url='/myadmin/accounts/login/')
def edit_hymn_view(request, hymn_id):
    ''' Edit the existing hymn

    '''
    if not request.user.has_perm(u'hymns.change_hymn') and not request.user.groups.filter(name='admins'):
        return render(request, 'hymns/test_result.html', {'result': '权限不够', })
    hymn = get_object_or_404(Hymn, pk=hymn_id)
    if request.method == 'POST':
        form = Hymn_Form(request.POST, request.FILES, instance=hymn)
        if form.is_valid():
            hymn = form.save(commit=False)
            if hymn.hymn_audio and not hymn.hymn_audio.lower().endswith('mp3'):
                tmp = re.findall('zanmeishi.com/song/(\d+)\.html',hymn.hymn_audio)
                if len(tmp) == 1:
                    audio_id = tmp[0]
                    hymn.hymn_audio = "http://api.zanmeishi.com/song/p/%s.mp3" % audio_id
                else:
                    return render(request, 'hymns/test_result.html', {'result': '链接地址不对', })
            hymn.save()
            form.save_m2m()
            print 'Hymn saved! %s' % hymn.id
            return HttpResponseRedirect(reverse('hymns:hymn', args=(hymn.id,)))
    else:
        form = Hymn_Form(instance=hymn)
    return render(request, 'myadmin/edit_hymn.html', {'hymn_form': form, })

@login_required(login_url='/myadmin/accounts/login/')
def hymns_view(request):
    if not request.user.groups.filter(name='admins'):
        return render(request, 'hymns/test_result.html', {'result': '权限不够', })
    hymns = Hymn.objects.all()
    return render(request, 'myadmin/all_hymns.html', {'hymns': hymns})

def login_view(request):
    if request.user is not None and request.user.is_active:
        return HttpResponseRedirect(reverse('myadmin:index'))
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    next_url = request.POST.get('next', '')
    if len(next_url) ==  0:
        next_url = request.GET.get('next', '')
        if len(next_url) == 0:
            next_url = reverse('myadmin:index')
    if next_url == reverse('myadmin:login_view'):
        next_url = reverse('myadmin:index')
    if user is not None and user.is_active:
        # Correct password, and the user is marked 'active'
        auth.login(request, user)
        # Redirect to a success page.
        return HttpResponseRedirect(next_url)
    else:
        # Show an error page
        return render(request, 'myadmin/login.html', {'next': next_url})

def logout_view(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('homepage:login_view'));

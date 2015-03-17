#!/usr/local/bin/python
# coding=utf-8
# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib import auth
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from hymns.models import Hymn_Key, Hymn, Weekly_Hymn, Hymn_Form, Worship_Location, Weekly_Hymn_Form

import json
import random

def index(request):
    all_hymns_list = Hymn.objects.filter(hymn_isCandidate=False).order_by('hymn_index')
    import math
    num_of_rows = int(math.ceil(len(all_hymns_list) / 3.0))
    context = {'all_hymns_list': all_hymns_list, 'num_of_rows': num_of_rows, }
    return render(request, 'hymns/index.html', context)
    # return render(request, 'hymns/foundation/index.html', context)

def hymn_by_key(request):
    key_list = Hymn_Key.objects.all()
    hymn_by_key_list = [x.hymn_set.all().order_by('hymn_index') for x in key_list]
    extra_list = []
    for hymn_list in hymn_by_key_list:
        extra = len(hymn_list) % 4
        if extra != 0:
            extra = 4 - extra;
        extra_list.append(range(0,extra))
    zipdata = zip(hymn_by_key_list, extra_list)
    return render(request, 'hymns/hymn_by_key.html', {'zipdata': zipdata})

def hymn(request, hymn_id):
    hymn = get_object_or_404(Hymn, pk=hymn_id)
    # print "http://%s%s" % (request.get_host(), request.get_full_path())
    # print request.build_absolute_uri()
    return render(request, 'hymns/hymn_detail.html', {'hymn': hymn})

def hymn_list_view(request, hymn_id, hymn_ids):
    ''' Show a hymn among a list of hymns.

    We need to compute the previous and the next hymns.
    '''
    hymn = get_object_or_404(Hymn, pk=hymn_id)
    hymn_id_list = hymn_ids.split('-')
    context = {'hymn': hymn, }
    try:
        index = hymn_id_list.index(hymn_id)
    except ValueError:
        return render(request, 'hymns/hymn_detail.html', context)
    else:
        context['hymn_ids'] = hymn_ids
        if index < len(hymn_id_list) - 1:
            context['next_hymn_id'] = hymn_id_list[index+1]
        if index > 0:
            context['previous_hymn_id'] = hymn_id_list[index-1]
        return render(request, 'hymns/hymn_detail.html', context)

# def weekly_hymns_json(request):
#     ''' Return the latest Weekly_Hymn
# 
#     '''
#     hymns = Weekly_Hymn.objects.all().order_by('-hymn_date', 'hymn_order')
#     response_json = {}
#     if hymns:
#         import datetime
#         tmp_date = hymns[0].hymn_date.strftime('%Y年%m月%d')
#         response_json['date'] = tmp_date
#         tmp_hymn_list = []
#         for hymn in hymns:
#             if tmp_date == hymn.hymn_date.strftime('%Y年%m月%d'):
#                 tmp_hymn_list.append("%s. %s" % (hymn.music.music_index, hymn.music.music_name))
#             else:
#                 response_json['hymn_list'] = tmp_hymn_list
#                 break
#     return HttpResponse(json.dumps(response_json), content_type="application/json")
# 
# def musics_json(request, music_index):
#     musics = Music.objects.filter(music_index=int(music_index))
#     response_json = {}
#     if len(musics) > 0:
#         music = musics[0]
#         audios =  music.audio_set.all()
#         if len(audios) > 0:
#             response_json['music_name'] = music.music_name
#             response_json['audio_description'] = audios[0].audio_name
#             response_json['audio_url'] = audios[0].audio_url
#     return HttpResponse(json.dumps(response_json), content_type="application/json")
# 

def weekly_hymns(request):
    return weekly_hymns_page(request, 1)

def weekly_hymns_page(request, page_num):
    tmp_dates = Weekly_Hymn.objects.dates('hymn_date', 'day', order='DESC')
    tmp_places = Worship_Location.objects.all()
    weekly_hymn_list = []
    if tmp_dates and tmp_places:
        for tmp_date in tmp_dates:
            hymn_by_place_list = []
            hymn_ids_by_place = []
            hymn_by_place_list.append(tmp_date.strftime('%Y年%m月%d'))
            tmp_hymn_by_place = []
            for tmp_place in tmp_places:
                tmp_hymns = list(tmp_place.weekly_hymn_set.filter(hymn_date=tmp_date).order_by('hymn_order'))
                tmp_hymn_by_place.append(tmp_hymns)
                hymn_ids_by_place.append('-'.join([str(h.hymn.id) for h in tmp_hymns]))
            hymn_by_place_list.append(zip(tmp_hymn_by_place,hymn_ids_by_place))
            weekly_hymn_list.append(hymn_by_place_list)
    # print weekly_hymn_list
    paginator = Paginator(weekly_hymn_list, 3)
    try:
        weekly_hymn_list = paginator.page(page_num)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        weekly_hymn_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range(e.g. 999999), deliver last page of results.
        weekly_hymn_list = paginator.page(paginator.num_pages)
    return render(request, 'hymns/weekly_hymns.html', {'weekly_hymn_list': weekly_hymn_list})

# Use homepage login and register
# def login_view(request):
#     if request.user is not None and request.user.is_active:
#         return HttpResponseRedirect(reverse('hymns:index'))
#     username = request.POST.get('username', '')
#     password = request.POST.get('password', '')
#     user = auth.authenticate(username=username, password=password)
#     next_url = request.POST.get('next', '')
#     if len(next_url) ==  0:
#         next_url = request.GET.get('next', '')
#         if len(next_url) == 0:
#             next_url = reverse('hymns:index')
#     if next_url == reverse('hymns:login_view'):
#         next_url = reverse('hymns:index')
#     if user is not None and user.is_active:
#         # Correct password, and the user is marked 'active'
#         auth.login(request, user)
#         # Redirect to a success page.
#         return HttpResponseRedirect(next_url)
#     else:
#         # Show an error page
#         return render(request, 'hymns/login.html', {'next': next_url})
# 
# def logout_view(request):
#     auth.logout(request)
#     return HttpResponseRedirect(reverse('hymns:login_view'));
# 
# def register_view(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             new_user = form.save()
#             return HttpResponseRedirect(reverse('hymns:logout_view'))
#     else:
#         form = UserCreationForm()
#     return render(request, 'hymns/register.html', { 'form': form, })

@login_required
def save_audio_url(request, hymn_id):
    if request.method == 'POST':
        if not request.user.groups.filter(name='uploaders') and not request.user.has_perm(u'hymns.change_hymn'):
            return render(request, 'hymns/test_result.html', {'result': '权限不够', })
        else:
            hymn = get_object_or_404(Hymn, pk=hymn_id)
            audio_url = request.POST.get('audioUrlInput', '')
            import re
            tmp = re.findall('zanmeishi.com/song/(\d+)\.html', audio_url)
            if len(tmp) == 1:
                audio_id = tmp[0]
                audio_url = "http://api.zanmeishi.com/song/p/%s.mp3" % audio_id
                print audio_url, request.user.username
                hymn.hymn_audio = audio_url
                hymn.hymn_audio_uploader_name = request.user.username
                hymn.save()
                return HttpResponseRedirect(reverse('hymns:hymn', args=(hymn.id,)))
            else:
                return render(request, 'hymns/test_result.html', {'result': '链接地址不对', })
    else:
        return HttpResponseRedirect(reverse('hymns:hymn', args=(hymn_id,)))

@login_required
def upload_hymn_view(request):
    ''' Upload the hymn

    '''
    if not request.user.groups.filter(name='uploaders') and not request.user.has_perm(u'hymns.add_hymn'):
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
    return render(request, 'hymns/upload_hymn.html', {'hymn_form': form, })

@login_required
def edit_hymn_view(request, hymn_id):
    '''Edit the hymn

    '''
    if not request.user.has_perm(u'hymns.change_hymn'):
        return render(request, 'hymns/test_result.html', {'result': '权限不够', })

    hymn = get_object_or_404(Hymn, pk=hymn_id)
    if request.method == 'POST':
        form = Hymn_Form(request.POST, request.FILES, instance=hymn)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('hymns:hymn', args=(hymn.id,)))
    else:
        form = Hymn_Form(instance=hymn)
    return render(request, 'hymns/upload_hymn.html', {'hymn_form': form, })

@login_required
def edit_weekly_hymn_view(request, weekly_hymn_id):
    '''Edit the weekly hymn for ppt and pdf

    '''
    if not request.user.has_perm(u'hymns.change_weekly_hymn'):
        return render(request, 'hymns/test_result.html', {'result': '权限不够', })

    weekly_hymn = get_object_or_404(Weekly_Hymn, pk=weekly_hymn_id)
    if request.method == 'POST':
        form = Weekly_Hymn_Form(request.POST, request.FILES, instance=weekly_hymn)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('hymns:weekly_hymns'))
    else:
        form = Weekly_Hymn_Form(instance=weekly_hymn)
    return render(request, 'hymns/upload_hymn.html', {'hymn_form': form, })

def candidates_view(request):
    candidate_hymn_list = Hymn.objects.filter(hymn_isCandidate=True)
    import math
    num_of_rows = int(math.ceil(len(candidate_hymn_list) / 3.0))
    context = {'candidate_hymn_list': candidate_hymn_list,  'num_of_rows': num_of_rows, }
    return render(request, 'hymns/candidates.html', context)

# def tmpScore(request, score_id, score_type):
#     context = {}
#     if score_type == 'candidate_score':
#         score = get_object_or_404(Candidate_Score, pk=score_id)
#         context['candidate_score'] = score
#     elif score_type == 'candidate_score_no_music':
#         score = get_object_or_404(Candidate_Score_No_Music, pk=score_id)
#         context['candidate_score_no_music'] = score
# 
#     if score.score_name.endswith('png') or score.score_name.endswith('jpg') or score.score_name.endswith('gif') or score.score_name.endswith('jpeg'):
#         isIMG = True
#     else:
#         isIMG = False
#     context['isIMG'] = isIMG
#     score.score_url = getTmpScoreUrl(score_id, score_type)
#     return render(request, 'musics/score_detail.html', context)
# 
# def getTmpScoreUrl(score_id, score_type):
#     from os import environ
#     online = environ.get('APP_NAME', '')
#     if score_type == 'candidate_score':
#         score = get_object_or_404(Candidate_Score, pk=score_id)
#         music = score.music
#     elif score_type == 'candidate_score_no_music':
#         score = get_object_or_404(Candidate_Score_No_Music, pk=score_id)
#         music = score.candidate_music
#     file_name = u'Tmp/%d.%s/%s' % (music.music_index, music.music_name, score.score_name)
# 
#     if online:
#         from sae.storage import Bucket, Connection
#         connection = Connection()
#         bucket = connection.get_bucket('score')
#         result = bucket.generate_url(file_name)
#     else:
#         result = file_name
# 
#     return result
# 
# def tmpMusic(request, music_id):
#     music = get_object_or_404(Candidate_Music, pk=music_id)
#     return render(request, 'musics/tmp_score_list.html', {'music': music})
# 
# def getScoreUrl(score_id):
#     from os import environ
#     online = environ.get('APP_NAME', '')
#     score = get_object_or_404(Score, pk=score_id)
#     music = score.music
#     file_name = u'MusicScores/%d.%s/%s' % (music.music_index, music.music_name, score.score_name)
# 
#     if online:
#         from sae.storage import Bucket, Connection
#         connection = Connection()
#         bucket = connection.get_bucket('score')
#         result = bucket.generate_url(file_name)
#     else:
#         result = file_name
# 
#     return result
# 
import re

from django.db.models import Q

def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:

        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']

    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 

def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.

    '''
    query = None # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query

def search(request):
    query_string = request.GET.get('queryString', '')
    found_entries = None
    if query_string:
        entry_query = get_query(query_string, ['hymn_name',])
        found_hymns = Hymn.objects.filter(entry_query).order_by('hymn_index')

    return render(request, 'hymns/search_results.html', { 'query_string': query_string, 'found_hymns': found_hymns, })


# def syncdb(request):
#     ''' run the 'python manage.py syncdb'
# 
#     '''
#     import sys
#     import StringIO
#     from django.http import HttpResponse
#     #重定向标准输出重定向到内存的字符串缓冲(由StringIO模块提供)
#     saveout = sys.stdout
#     log_out = StringIO.StringIO()
#     sys.stdout = log_out 
#     #利用django提供的命令行工具来执行“manage.py syncdb”
#     from django.core.management import execute_from_command_line
#     execute_from_command_line(["manage.py", "syncdb", "--noinput"])
#     #获得“manage.py syncdb”的执行输出结果，并展示在页面
#     result = log_out.getvalue()
#     sys.stdout = saveout
#     return HttpResponse(result.replace("\n","<br/>"))

def playlist_view(request):
    # For efficiency
    # all_hymns_list = Hymn.objects.exclude(hymn_audio__isnull=True).exclude(hymn_audio__exact='').order_by('?')
    hymns = Hymn.objects.exclude(hymn_audio__isnull=True).exclude(hymn_audio__exact='')
    last = hymns.count() - 1
    hymn = hymns[random.randint(0, last)]
    context = {'hymn': hymn,}
    return render(request, 'hymns/hymn_playlist.html', context)

def random_hymn_json(request):
    response_json = {}
    hymns = Hymn.objects.exclude(hymn_audio__isnull=True).exclude(hymn_audio__exact='')
    last = hymns.count() - 1
    hymn = hymns[random.randint(0, last)]
    response_json['hymn_name'] = hymn.hymn_name
    response_json['hymn_audio'] = hymn.hymn_audio
    response_json['hymn_score'] = hymn.hymn_score.url
    return HttpResponse(json.dumps(response_json), content_type="application/json")

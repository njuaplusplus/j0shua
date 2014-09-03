#!/usr/bin/python
# coding=utf-8
# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib import auth
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse

from hymns.models import Hymn_Key, Hymn, Weekly_Hymn, Candidate_Hymn

import json

def index(request):
    all_hymns_list = Hymn.objects.all().order_by('hymn_index')
    import math
    num_of_rows = int(math.ceil(len(all_hymns_list) / 3.0))
    context = {'all_hymns_list': all_hymns_list, 'num_of_rows': num_of_rows, }
    return render(request, 'hymns/index.html', context)

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
    return render(request, 'hymns/hymn_detail.html', {'hymn': hymn})

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
    hymns = Weekly_Hymn.objects.all().order_by('-hymn_date', 'hymn_order')
    weekly_hymn_list = []
    if hymns:
        import datetime
        tmp_date = hymns[0].hymn_date.strftime('%Y年%m月%d')
        tmp_hymn_list = [tmp_date]
        for hymn in hymns:
            if tmp_date == hymn.hymn_date.strftime('%Y年%m月%d'):
                tmp_hymn_list.append(hymn)
            else:
                weekly_hymn_list.append(tmp_hymn_list)
                print 'weekly_hymn_list appended', weekly_hymn_list
                tmp_date = hymn.hymn_date.strftime('%Y年%m月%d')
                tmp_hymn_list = [tmp_date, hymn]
        if tmp_hymn_list:
            weekly_hymn_list.append(tmp_hymn_list)
    return render(request, 'hymns/weekly_hymns.html', {'weekly_hymn_list': weekly_hymn_list})

def login_view(request):
    if request.user is not None and request.user.is_active:
        return HttpResponseRedirect(reverse('hymns:index'))
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    next_url = request.POST.get('next', '')
    if len(next_url) ==  0:
        next_url = request.GET.get('next', '')
        if len(next_url) == 0:
            next_url = reverse('hymns:index')
    if next_url == reverse('hymns:login_view'):
        next_url = reverse('hymns:index')
    if user is not None and user.is_active:
        # Correct password, and the user is marked 'active'
        auth.login(request, user)
        # Redirect to a success page.
        return HttpResponseRedirect(next_url)
    else:
        # Show an error page
        return render(request, 'hymns/login.html', {'next': next_url})

def logout_view(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('hymns:login_view'));

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect(reverse('hymns:logout_view'))
    else:
        form = UserCreationForm()
    return render(request, 'hymns/register.html', { 'form': form, })
# 
@login_required(login_url='/hymns/accounts/login/')
def upload_view(request):
    return HttpResponse("Hello, world. You're at the poll index.")
#     #if not request.user.has_perm('musics.add_candidate_score'):
#     if not request.user.groups.filter(name='uploaders'):
#         return render(request, 'musics/test_result.html', {'result': '权限不够', })
#     music_list = Music.objects.all().order_by('music_index')
#     music_key_list = Music_Key.objects.all()
#     return render(request, 'musics/upload.html', {'music_list': music_list, 'music_key_list': music_key_list,})
# 
# @login_required
# def saveScoreFile(request, upload_type):
#     if request.method == 'POST':
#         #if not request.user.has_perm('musics.add_candidate_score'):
#         if not request.user.groups.filter(name='uploaders'):
#             return render(request, 'musics/test_result.html', {'result': '权限不够', })
# 
#         #upload_type = request.POST.get('optionsRadios', '')
# 
#         content = request.FILES['scoreInputFile']
# 
#         if upload_type == 'candidate_score':
#             music_id = request.POST.get('music_id', '')
#             music = get_object_or_404(Music, pk=music_id)
#             file_name = u'Tmp/%d.%s/%s' % (music.music_index, music.music_name, content.name)
#         elif upload_type == 'candidate_score_no_music':
#             music_index = int(request.POST.get('candidateMusicIndexInput', ''))
#             music_name = request.POST.get('candidateMusicNameInput', '')
#             music_key_id = request.POST.get('music_key_id', '')
#             music_key = get_object_or_404(Music_Key, pk=music_key_id)
#             candidate_music = Candidate_Music.objects.get_or_create(music_index=music_index, music_name=music_name, music_key=music_key, uploader=request.user)[0]
#             file_name = u'Tmp/%d.%s/%s' % (candidate_music.music_index, candidate_music.music_name, content.name)
#         else:
#             return render(request, 'musics/test_result.html', {'result': u'需要选择一种上传方式%s' % upload_type, })
# 
#         from os import environ
#         online = environ.get('APP_NAME', '')
# 
#         if online:
#             if upload_type == 'candidate_score':
#                 music.candidate_score_set.create(score_name=content.name, score_url=content.name, uploader=request.user)
#             elif upload_type == 'candidate_score_no_music':
#                 candidate_music.candidate_score_no_music_set.create(score_name=content.name, score_url=content.name, uploader=request.user)
#             from sae.storage import Bucket, Connection
#             connection = Connection()
#             bucket = connection.get_bucket('score')
#             bucket.put_object(file_name, content)
#             result = bucket.generate_url(file_name)
#             return HttpResponseRedirect(reverse('musics:candidates_view'))
#         else:
#             result = 'test haha file_name: %s' % file_name
# 
#         return render(request, 'musics/test_result.html', {'result': result, })
#     else:
#         return HttpResponseRedirect(reverse('musics:upload_view'))
# 
def candidates_view(request):
    return HttpResponse("Hello, world. You're at the poll index.")
#     candidate_music_list = Candidate_Music.objects.all()
#     candidate_score_no_music_list = Candidate_Score_No_Music.objects.all()
#     candidate_score_list = Candidate_Score.objects.all()
#     context = {'candidate_music_list': candidate_music_list, 'candidate_score_no_music_list': candidate_score_no_music_list, 'candidate_score_list': candidate_score_list, }
#     return render(request, 'musics/candidates.html', context)
# 
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
# import re
# 
# from django.db.models import Q
# 
# def normalize_query(query_string,
#                     findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
#                     normspace=re.compile(r'\s{2,}').sub):
#     ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
#         and grouping quoted words together.
#         Example:
# 
#         >>> normalize_query('  some random  words "with   quotes  " and   spaces')
#         ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
# 
#     '''
#     return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 
# 
# def get_query(query_string, search_fields):
#     ''' Returns a query, that is a combination of Q objects. That combination
#         aims to search keywords within a model by testing the given search fields.
# 
#     '''
#     query = None # Query to search for every search term
#     terms = normalize_query(query_string)
#     for term in terms:
#         or_query = None # Query to search for a given term in each field
#         for field_name in search_fields:
#             q = Q(**{"%s__icontains" % field_name: term})
#             if or_query is None:
#                 or_query = q
#             else:
#                 or_query = or_query | q
#         if query is None:
#             query = or_query
#         else:
#             query = query & or_query
#     return query
# 
def search(request):
    return HttpResponse("Hello, world. You're at the poll index.")
#     query_string = request.GET.get('queryString', '')
#     found_entries = None
#     if query_string:
#         entry_query = get_query(query_string, ['music_name',])
#         found_musics = Music.objects.filter(entry_query).order_by('music_index')
# 
#     return render(request, 'musics/search_results.html', { 'query_string': query_string, 'found_musics': found_musics, })
# 
# 
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

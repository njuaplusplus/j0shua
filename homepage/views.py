#!/usr/local/bin/python
# coding=utf-8
from django.shortcuts import render, redirect

# Create your views here.

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib import auth
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
# from django.utils import timezone
from django.conf import settings  # use settings
import datetime
import random
import urllib.parse
import hashlib
import requests

from bibles.models import Bible_CHN, Daily_Verse, Weekly_Verse, Weekly_Reading, Weekly_Recitation
from hymns.models import Weekly_Hymn, Worship_Location
from homepage.models import User_Profile


def index(request):
    # today = timezone.now().date() # 8 hours earlier
    today = datetime.date.today()
    coming_sunday = today + datetime.timedelta(days=6-today.weekday())
    last_sunday = today - datetime.timedelta(days=today.weekday()+1)
    daily_verse = Daily_Verse.objects.filter(verse_date=today).first()
    weekly_verse = Weekly_Verse.objects.filter(verse_date=coming_sunday).first()
    weekly_readings = list(Weekly_Reading.objects.filter(verse_date__range=(last_sunday,coming_sunday)).order_by('-verse_date'))
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
    # For Weekly Hymns
    weekly_hymns = []
    weekly_hymn_ids = []
    db_weekly_hymns = Weekly_Hymn.objects.filter(hymn_date=coming_sunday)
    if db_weekly_hymns:
        places = Worship_Location.objects.all()
        for place in places:
            weekly_hymns_by_place = []
            tmp_hymns = db_weekly_hymns.filter(hymn_place=place).order_by('hymn_order')
            for h in tmp_hymns:
                weekly_hymns_by_place.append(h)
            weekly_hymn_ids.append('-'.join([str(h.hymn.id) for h in weekly_hymns_by_place]))
            weekly_hymns.append(weekly_hymns_by_place)
    context = {
        'daily_verses' : list(daily_verses),
        'weekly_verses': list(weekly_verses),
        'weekly_hymns': list(zip(weekly_hymns,weekly_hymn_ids)),
        'weekly_readings': weekly_readings,
        'weekly_recitation_verses': weekly_recitation_verses,
    }
    return render(request, 'homepage/index.html', context)


def about_view(request):
    return render(request, 'homepage/about.html')


def decide_next_url(next_url):
    if next_url is None or len(next_url) == 0 or next_url == reverse('homepage:login_view') or next_url == reverse('homepage:register_view'):
        next_url = reverse('homepage:index')
    return next_url


def login_view(request):
    if request.user is not None and request.user.is_active:
        return HttpResponseRedirect(reverse('homepage:index'))
    if request.method == 'POST': # 本地用户登录
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        next_url = decide_next_url(request.POST.get('next', ''))
        if user is not None and user.is_active:
            # Correct password, and the user is marked 'active'
            auth.login(request, user)
            return HttpResponseRedirect(next_url)
        else:
            # Show an error page
            return render(request, 'homepage/login.html', {'next': next_url})
    else: # GET method
        next_url = decide_next_url(request.GET.get('next', ''))
        return render(
            request,
            'homepage/login.html',
            {
                'next': next_url,
                'wechat_appid': settings.WECHAT_APP_ID,
                'wechat_scope': 'snsapi_login',
                'wechat_redirect_url': calculate_wechat_redirect_url(request),
                'wechat_state': calculate_wechat_state()
            }
        )


def logout_view(request):
    auth.logout(request)
    response = HttpResponseRedirect(reverse('homepage:login_view'))
    return response


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect(reverse('homepage:logout_view'))
    else:
        form = UserCreationForm()
    return render(request, 'homepage/register.html', { 'form': form, })


def page_not_found_view(request):
    ''' Custom 404 page
    '''
    response = render(request, '404.html')
    response.status_code = 404
    return response


def calculate_wechat_state():
    return hashlib.sha256(
        (datetime.date.today().ctime() + settings.WECHAT_STATE_SEED).encode('utf-8')).hexdigest()


def calculate_wechat_redirect_url(request):
    redirect_url = request.is_secure() and 'https://' or 'http://'
    redirect_url += request.get_host() + reverse('homepage:wechat_login_view')
    redirect_url = urllib.parse.quote(redirect_url, safe='')
    return redirect_url


def wechat_login_view(request):
    code = request.GET.get('code', '')
    state = request.GET.get('state', '')
    calculated_state = calculate_wechat_state()
    if code:
        if state != calculated_state:
            return redirect(reverse('homepage:login_view'))
        else:
            # get the user info
            res = requests.get(
                'https://api.weixin.qq.com/sns/oauth2/access_token',
                params={
                    'appid':      settings.WECHAT_APP_ID,
                    'secret':     settings.WECHAT_APP_SECRET,
                    'code':       code,
                    'grant_type': 'authorization_code'
                }
            )
            if res.status_code == 200:
                res = res.json()
                access_token = res['access_token']
                openid = res['openid']
                username = 'WX' + openid
                user = User.objects.filter(username=username).first()
                if user:
                    if user.is_active:
                        user.backend = 'django.contrib.auth.backends.ModelBackend'
                        auth.login(request, user)
                        return HttpResponseRedirect(reverse('homepage:index'))
                else:
                    res = requests.get(
                        'https://api.weixin.qq.com/sns/userinfo',
                        params={
                            'access_token': access_token,
                            'openid': openid
                        }
                    )
                    if res.status_code == 200:
                        res = res.json()
                        unionid = res['unionid']
                        avatar = res['headimgurl']
                        nickname = res['nickname'].encode('latin-1').decode('utf-8')
                        password = ''.join([random.choice('abcdefghijklmnopqrstuvwxyz!@#$%^&*ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(12)])
                        user = User.objects.create_user(username=username, password=password, first_name=nickname)
                        User_Profile.objects.create(user=user, avatar=avatar, unionid=unionid, openid=openid)
                        user.backend = 'django.contrib.auth.backends.ModelBackend'
                        auth.login(request, user)
                        return HttpResponseRedirect(reverse('homepage:index'))
    else:

        return redirect(
            "https://open.weixin.qq.com/connect/qrconnect?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_login&state=%s#wechat_redirect" %
            (settings.WECHAT_APP_ID, calculate_wechat_redirect_url(request), calculated_state))


def print_request(request):
    print(request.GET)
    print(request.get_full_path())
    print(request.get_host())
    print(request.is_secure())
    return HttpResponse('ok')
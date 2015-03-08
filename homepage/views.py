#!/usr/local/bin/python
# coding=utf-8
from django.shortcuts import render

# Create your views here.

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib import auth
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
# from django.utils import timezone
from django.conf import settings # use settings
import datetime
import jwt
import random
from duoshuo import DuoshuoAPI

from bibles.models import Bible_CHN, Daily_Verse, Weekly_Verse, Weekly_Reading, Weekly_Recitation
from hymns.models import Weekly_Hymn, Worship_Location
from homepage.models import User_Profile

def index(request):
    # today = timezone.now().date() # 8 hours earlier
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
    # For Weekly Hymns
    weekly_hymns = []
    db_weekly_hymns = Weekly_Hymn.objects.filter(hymn_date=coming_sunday)
    if db_weekly_hymns:
        places = Worship_Location.objects.all()
        for place in places:
            weekly_hymns_by_place = []
            tmp_hymns = db_weekly_hymns.filter(hymn_place=place).order_by('hymn_order')
            for h in tmp_hymns:
                weekly_hymns_by_place.append(h)
            weekly_hymns.append(weekly_hymns_by_place)
    context = {'daily_verses' : list(daily_verses), 'weekly_verses': list(weekly_verses), 'weekly_hymns': weekly_hymns, 'weekly_readings': weekly_readings, 'weekly_recitation_verses': weekly_recitation_verses,}
    response = render(request, 'homepage/index.html', context)
    return set_jwt_and_response(request.user, response)

def about_view(request):
    return render(request, 'homepage/about.html')

def decide_next_url(next_url):
    if next_url is None or len(next_url) == 0 or next_url == reverse('homepage:login_view') or next_url == reverse('homepage:register_view'):
        next_url = reverse('homepage:index')
    return next_url

def login_view(request):
    if request.user is not None and request.user.is_active:
        response = HttpResponseRedirect(reverse('homepage:index'))
        return set_jwt_and_response(request.user, response)
    if request.method == 'POST': # 本地用户登录
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        next_url = decide_next_url(request.POST.get('next', ''))
        if user is not None and user.is_active:
            # Correct password, and the user is marked 'active'
            auth.login(request, user)
            response = HttpResponseRedirect(next_url)
            return set_jwt_and_response(request.user, response)
        else:
            # Show an error page
            return render(request, 'homepage/login.html', {'next': next_url})
    else: # GET method
        code = request.GET.get('code', '')
        next_url = decide_next_url(request.GET.get('next', ''))
        if len(code) > 0: # 多说登录
            api = DuoshuoAPI(settings.DUOSHUO_SHORT_NAME, settings.DUOSHUO_SECRET)
            response = api.get_token(code=code)
            print 'api.get_token %s' % code
            print response
            if response.has_key('user_key'): # 这个多说账号已经绑定过本地账户了
                user = User.objects.get(pk=int(response['user_key']))
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                auth.login(request, user)
                user_profile = User_Profile.objects.filter(user=user)
                if not user_profile: # 手动绑定了多说账号和本地账号, 但是本地没有对应的 user_profile
                    user_profile = User_Profile(user=user,duoshuo_id=int(response['user_id']), avatar=response['avatar_url'])
                    user_profile.save()
            else: # 这个多说账户还没有绑定
                access_token = response['access_token']
                user_profile = User_Profile.objects.filter(duoshuo_id=int(response['user_id']))
                if user_profile: #此多说账号在本站已经注册过了, 但是没有绑定, 则先绑定, 然后直接登录
                    user = user_profile.first().user
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    auth.login(request, user)
                else: # 此多说账号在本站未注册, 添加一个用户
                    print 'api.users.profile user_id %s' % response['user_id']
                    response = api.users.profile(user_id=response['user_id'])['response']
                    print response
                    username = 'duoshuo_%s' % response['user_id']
                    while User.objects.filter(username=username).count():
                        username = username + str(random.randrange(1,9)) #如果多说账号用户名和本站用户名重复，就加上随机数字
                    tmp_password = ''.join([random.choice('abcdefg&#%^*f') for i in range(8)]) #随机长度8字符做密码
                    new_user = User.objects.create_user(username=username, email='user@example.com', password=tmp_password, first_name=response['name']) #默认密码和邮箱，之后让用户修改
                    user_profile = User_Profile.objects.get_or_create(user=new_user)[0]
                    user_profile.duoshuo_id = int(response['user_id']) #把返回的多说ID存到profile
                    user_profile.avatar = response['avatar_url']
                    user_profile.save()

                    user = auth.authenticate(username=username, password=tmp_password)
                    auth.login(request, user)
                # SSO 同步多说账户
                sync_sso_duoshuo(access_token, request.user)
            response = HttpResponseRedirect(next_url)
            return set_jwt_and_response(request.user, response)
        # absolute_next_url = request.build_absolute_uri(next_url)
        sso_login_url = '%s?next=%s' % (request.build_absolute_uri(reverse('homepage:login_view')), next_url)
        sso_logout_url = request.build_absolute_uri(reverse('homepage:logout_view'))
        context = {'next': next_url, 'sso_login_url': sso_login_url, 'sso_logout_url': sso_logout_url, }
        return render(request, 'homepage/login.html', context)

def logout_view(request):
    print 'logout_view'
    auth.logout(request)
    response = HttpResponseRedirect(reverse('homepage:login_view'))
    response.delete_cookie('duoshuo_token')
    print 'return logout_view'
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

def set_jwt_and_response(user, response):
    # For duoshuo jwt login
    if user is not None and user.is_authenticated() and user.is_active:
        user_profile = User_Profile.objects.filter(user=user)
        if not user_profile: # 本地的没有 多说 User_Profile
            # 则使用 jwt 来创建一个多说账户
            # For duoshuo jwt login
            duoshuo_jwt_token = None
            username = user.get_full_name()
            if not username:
                username = user.username
            token = {
                "short_name": settings.DUOSHUO_SHORT_NAME,
                "user_key": user.id,
                "name": username
            }
            duoshuo_jwt_token = jwt.encode(token, settings.DUOSHUO_SECRET)
            response.set_cookie('duoshuo_token', duoshuo_jwt_token)
    return response

import urllib
import urllib2

def sync_sso_duoshuo(access_token, user):
    '''将SSO本地用户同步到已有多说账户中
    '''
    url = 'http://api.duoshuo.com/sites/join.json'
    username = user.get_full_name()
    if not username:
        username = user.username
    email = user.email
    if not email:
        email = 'user@example.com'
    params = {
        'short_name': settings.DUOSHUO_SHORT_NAME,
        'secret': settings.DUOSHUO_SECRET,
        'access_token': access_token,
        'user[user_key]': user.id,
        'user[name]': username,
        'user[email]': user.email,
    }
    print 'sync_sso_duoshuo'
    print params
    data = urllib.urlencode(params)
    request = urllib2.Request(url, data=data)
    response = urllib2.urlopen(request)
    result = response.read()
    print result

def page_not_found_view(request):
    ''' Custom 404 page
    '''
    response = render(request, '404.html')
    response.status_code = 404
    return response

#!/usr/local/bin/python
# coding=utf-8
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import auth
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from hymns.models import Weekly_Hymn, Hymn, Worship_Location
from blog.models import Article, ArticleForm

import datetime
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

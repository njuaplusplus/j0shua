from django.shortcuts import render

# Create your views here.

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib import auth
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse
from django.utils import timezone
import datetime

from bibles.models import Bible_CHN, Daily_Verse
from hymns.models import Weekly_Hymn, Worship_Location

def index(request):
    today = timezone.now().date()
    # For Daily verse
    daily_verse = Daily_Verse.objects.order_by('-verse_date').first()
    verses = None
    if daily_verse:
        # Get the daily verses
        verses = Bible_CHN.objects.filter(pk__range=(daily_verse.start_verse.id, daily_verse.end_verse.id)).order_by('pk')
    # For Weekly Hymns
    weekly_hymns = []
    coming_sunday = today + datetime.timedelta(days=6-today.weekday())
    db_weekly_hymns = Weekly_Hymn.objects.filter(hymn_date=coming_sunday)
    if db_weekly_hymns:
        places = Worship_Location.objects.all()
        for place in places:
            weekly_hymns_by_place = []
            tmp_hymns = db_weekly_hymns.filter(hymn_place=place).order_by('hymn_order')
            for h in tmp_hymns:
                weekly_hymns_by_place.append(h)
            weekly_hymns.append(weekly_hymns_by_place)
    context = {'verses' : list(verses), 'weekly_hymns': weekly_hymns}
    return render(request, 'homepage/index.html', context)

def login_view(request):
    if request.user is not None and request.user.is_active:
        return HttpResponseRedirect(reverse('homepage:index'))
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    next_url = request.POST.get('next', '')
    if len(next_url) ==  0:
        next_url = request.GET.get('next', '')
        if len(next_url) == 0:
            next_url = reverse('homepage:index')
    if next_url == reverse('homepage:login_view'):
        next_url = reverse('homepage:index')
    if user is not None and user.is_active:
        # Correct password, and the user is marked 'active'
        auth.login(request, user)
        # Redirect to a success page.
        return HttpResponseRedirect(next_url)
    else:
        # Show an error page
        return render(request, 'homepage/login.html', {'next': next_url})

def logout_view(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('homepage:login_view'));

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect(reverse('homepage:logout_view'))
    else:
        form = UserCreationForm()
    return render(request, 'homepage/register.html', { 'form': form, })

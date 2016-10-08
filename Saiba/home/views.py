from django.shortcuts import render, get_object_or_404, redirect
from django.utils.html import escape
from django.contrib.auth.models import Permission, User
from entry.models import Entry
from profile.models import Profile
from django.contrib.auth import authenticate, login, logout

def index(request):
    entries = Entry.objects.all()
    return render(request, 'home/index.html', {'entries': entries})

def user_login(request):
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('home:index')

    return render(request, 'home/login.html')

def user_logout(request):
    if request.user.is_authenticated():
        logout(request)

    return redirect('home:index')

def user_register(request):
    if request.user.is_authenticated():
        logout(request)

    return redirect('home:index')
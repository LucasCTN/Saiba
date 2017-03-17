from django.shortcuts import render, get_object_or_404
from .models import Profile

def index(request, name_slug):
    profile = get_object_or_404(Profile, slug=name_slug)

    context = { "profile": profile }
    return render(request, 'profile/index.html', context)

def detail(request, name_slug):
    profile = get_object_or_404(Profile, slug=name_slug)

    context = { "profile": profile, 'type': 'profile', "id": profile.user.id}
    return render(request, 'profile/detail.html', context)
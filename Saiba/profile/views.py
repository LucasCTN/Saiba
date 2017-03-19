from django.shortcuts import render, get_object_or_404
from .models import Profile
from entry.models import Entry
from gallery.models import Image, Video

def index(request, name_slug):
    profile = get_object_or_404(Profile, slug=name_slug)

    context = { "profile": profile }
    return render(request, 'profile/index.html', context)

def detail(request, name_slug):
    profile = get_object_or_404(Profile, slug=name_slug)

    context = { "profile": profile, 'type': 'profile', "id": profile.user.id}
    return render(request, 'profile/detail.html', context)

def editorships(request, name_slug):
    profile = get_object_or_404(Profile, slug=name_slug)
    entries = Entry.objects.filter(author=profile.user)

    context = { "profile": profile, 'type': 'profile', "id": profile.user.id, "entries": entries}
    return render(request, 'profile/editorship.html', context)

def images(request, name_slug):
    profile = get_object_or_404(Profile, slug=name_slug)
    images = Image.objects.filter(author=profile.user)

    context = { "profile": profile, 'type': 'profile', "id": profile.user.id, "images": images}
    return render(request, 'profile/images.html', context)

def videos(request, name_slug):
    profile = get_object_or_404(Profile, slug=name_slug)
    videos = Video.objects.filter(author=profile.user)

    context = { "profile": profile, 'type': 'profile', "id": profile.user.id, "videos": videos}
    return render(request, 'profile/videos.html', context)
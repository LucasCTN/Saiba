from django.shortcuts import render, get_object_or_404
from .models import Profile
from entry.models import Entry
from gallery.models import Image, Video
from feedback.models import Action

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

    context = {"profile": profile, 'type': 'profile', "id": profile.user.id, "videos": videos}
    return render(request, 'profile/videos.html', context)

def activity(request, name_slug, page = 1):
    profile = get_object_or_404(Profile, slug=name_slug)
    actions = Action.objects.filter(author=profile.user).order_by("-id")
    
    for action in actions:
        action.actor = action.author.profile
        action.location = action.target   

        if action.action_type == "1":
            action.message = action.target.content
            action.location = action.target.target #action -> comment -> (entry/image/video/profile)
        elif action.action_type == "2":
            action.message = action.target.content
            action.location = action.target.target #action -> reply -> (entry/image/video/profile)
            action.victim = action.target.reply_to.author

        if type(action.location) == Entry:
            action.location_type = "entry"
        elif type(action.location) == Image:
            action.location_type = "image"
        elif type(action.location) == Video:
            action.location_type = "video"
        elif type(action.location) == Profile:
            action.location_type = "profile"

    context = { "profile": profile, 'type': 'profile', "id": profile.user.id, "actions": actions}
    return render(request, 'profile/activity.html', context)
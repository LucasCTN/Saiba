from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.utils.html import escape
from django.core.urlresolvers import reverse
from .models import Image, Video
from .forms import ImageForm, VideoForm

def index(request):
    return render(request, 'entry/index.html')

def image_detail(request, image_id):
    image = get_object_or_404(Image, pk=image_id)

    args = {'image': image,
            'comments':comments}

    return render(request, 'gallery/image.html', {'image': image})

def video_detail(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    return render(request, 'gallery/video.html', {'video': video})

def historic(request, entry_slug):
    entry = get_object_or_404(Entry, slug=entry_slug)
    revisions = Revision.objects.filter(entry=entry, hidden=False)
    return render(request, 'entry/historic.html', {'revisions': revisions, 'entry_name':entry.title})

def revision(request, revision_id):
    revision = get_object_or_404(Revision, hidden=False, pk=revision_id)
    return render(request, 'entry/revision.html', {'revision': revision})

def upload_image(request):
    image_form = ImageForm(request.POST or None)

    if image_form.is_valid():
        image_form = ImageForm(request.POST, request.FILES)
        image = image_form.save()
        return render(request, 'gallery/image.html', {'image': image})

    return render(request, 'gallery/upload-image.html', {"form": image_form})

def upload_video(request):
    video_form = VideoForm(request.POST or None)

    if video_form.is_valid():
        video_form = VideoForm(request.POST, request.FILES)
        video = video_form.save()
        return render(request, 'gallery/video.html', {'video': video})

    return render(request, 'gallery/upload-video.html', {"form": video_form})
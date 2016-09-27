from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.utils.html import escape
from django.core.urlresolvers import reverse
from .models import Image

def index(request):
    return render(request, 'entry/index.html')

def image_detail(request, image_id):
    image = get_object_or_404(Image, pk=image_id)
    return render(request, escape('gallery/image.html'), {'image': image})

def historic(request, entry_slug):
    entry = get_object_or_404(Entry, slug=entry_slug)
    revisions = Revision.objects.filter(entry=entry, hidden=False)
    return render(request, escape('entry/historic.html'), {'revisions': revisions, 'entry_name':entry.title})

def revision(request, revision_id):
    revision = get_object_or_404(Revision, hidden=False, pk=revision_id)
    return render(request, escape('entry/revision.html'), {'revision': revision})

def upload_image(request):
    return render(request, escape('gallery/upload-image.html'))

def upload_video(request):
    return render(request, escape('gallery/upload-video.html'))
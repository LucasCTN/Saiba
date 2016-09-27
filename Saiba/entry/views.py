# -*- coding: utf-8 -*-
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
#from .forms import AlbumForm, SongForm, UserForm
from .models import Entry, Revision, Category
from django.utils.html import escape
from django.core.urlresolvers import reverse
from entry.serializers import EntrySerializer, RevisionSerializer
from gallery.models import Image

def index(request):
    '''if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        albums = Album.objects.filter(user=request.user)
        song_results = Song.objects.all()
        query = request.GET.get("q")
        if query:
            albums = albums.filter(
                Q(album_title__icontains=query) |
                Q(artist__icontains=query)
            ).distinct()
            song_results = song_results.filter(
                Q(song_title__icontains=query)
            ).distinct()
            return render(request, 'music/index.html', {
                'albums': albums,
                'songs': song_results,
            })
        else:
    return render(request, 'music/index.html', {'albums': albums})'''
    return render(request, 'entry/index.html')

def detail(request, entry_slug):
    '''if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        user = request.user
        album = get_object_or_404(Album, pk=album_id)
        return render(request, 'music/detail.html', {'album': album, 'user': user})'''
    entry = get_object_or_404(Entry, slug=entry_slug)
    last_revision = Revision.objects.filter(entry=entry, hidden=False).latest('pk')
    first_revision = Revision.objects.filter(entry=entry, hidden=False).earliest('pk')
    last_images = Image.objects.filter(hidden=False).order_by('-id')[:10]
    return render(request, escape('entry/detail.html'), {'entry': entry, 'last_revision':last_revision, 
                                                   'first_revision':first_revision, 'images':last_images})

def historic(request, entry_slug):
    entry = get_object_or_404(Entry, slug=entry_slug)
    revisions = Revision.objects.filter(entry=entry, hidden=False)
    return render(request, escape('entry/historic.html'), {'revisions': revisions, 'entry_name':entry.title})

def revision(request, revision_id):
    revision = get_object_or_404(Revision, hidden=False, pk=revision_id)
    return render(request, escape('entry/revision.html'), {'revision': revision})

def create_entry(request):
    categories = Category.objects.all()
    entries = Entry.objects.all()
    return render(request, escape('entry/create-entry.html'), {'categories': categories, 'entries': entries})
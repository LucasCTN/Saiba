# -*- coding: utf-8 -*-
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
#from .forms import AlbumForm, SongForm, UserForm
from .models import Entry, Revision, Category
from .forms import EntryForm, RevisionForm, CommentForm
from django.utils.html import escape
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
from entry.serializers import EntrySerializer, RevisionSerializer
from gallery.models import Image, Video
from feedback.models import Comment

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
    last_videos = Video.objects.filter(hidden=False).order_by('-id')[:10]

    comment_form = CommentForm(request.POST or None)
    
    raw_parent_comments = Comment.objects.filter(entry=entry, parent_comment=None, hidden=False).order_by('creation_date')
    raw_reply_comments = Comment.objects.filter(Q(entry=entry) & Q(hidden=False) & ~Q(parent_comment=None)).order_by('creation_date')

    comments = dict()

    for comment in raw_parent_comments:
        comments[comment] = list()

    for reply in raw_reply_comments:
        comments[reply.parent_comment].append(reply)

    args = {'entry': entry, 
            'last_revision':last_revision,                                                   
            'first_revision':first_revision, 
            'images':last_images,
            'videos':last_videos,
            'comments':comments}

    if comment_form.is_valid():
        comment_form = CommentForm(request.POST)        
        comment = comment_form.save(commit=False)
        comment.entry = entry
        comment.save()

    return render(request, escape('entry/detail.html'), args)

def history(request, entry_slug):
    entry = get_object_or_404(Entry, slug=entry_slug)
    revisions = Revision.objects.filter(entry=entry, hidden=False).order_by('-id')
    return render(request, escape('entry/history.html'), {'revisions': revisions, 'entry_name':entry.title, 'entry_slug':entry.slug})

def edit(request, entry_slug):
    entry = Entry.objects.get(slug=entry_slug)
    last_revision = Revision.objects.filter(entry=entry, hidden=False).latest('pk')
    first_revision = Revision.objects.filter(entry=entry, hidden=False).earliest('pk')

    entry_form = EntryForm(request.POST or None, initial=model_to_dict(entry))
    revision_form = RevisionForm(request.POST or None, initial=model_to_dict(last_revision))

    if entry_form.is_valid() and revision_form.is_valid():
        entry_form = EntryForm(request.POST, instance = entry)
        entry_form.save()

        revision = revision_form.save(commit=False)
        revision.entry = entry
        revision.save()

        last_revision = Revision.objects.filter(entry=entry, hidden=False).latest('pk')
        
        last_images = Image.objects.filter(hidden=False).order_by('-id')[:10]
        return render(request, 'entry/detail.html', {'entry': entry, 'last_revision':last_revision, 
                                                   'first_revision':first_revision, 'images':last_images})

    context = { "entry_form": entry_form, "revision_form": revision_form, "entry":entry }

    return render(request, 'entry/edit.html', context)

def revision(request, entry_slug, revision_id):
    revision = get_object_or_404(Revision, hidden=False, pk=revision_id)
    return render(request, escape('entry/revision.html'), { 'revision': revision })

def create_entry(request):
    entry_form = EntryForm(request.POST or None)
    revision_form = RevisionForm(request.POST or None)

    if entry_form.is_valid() and revision_form.is_valid():
        entry = entry_form.save(commit=False)
        entry.save()

        revision = revision_form.save(commit=False)
        revision.entry = entry
        revision.save()

        last_revision = Revision.objects.filter(entry=entry, hidden=False).latest('pk')
        first_revision = Revision.objects.filter(entry=entry, hidden=False).earliest('pk')
        last_images = Image.objects.filter(hidden=False).order_by('-id')[:10]
        return render(request, 'entry/detail.html', {'entry': entry, 'last_revision':last_revision, 
                                                   'first_revision':first_revision, 'images':last_images})

    context = { "entry_form": entry_form, "revision_form": revision_form }

    return render(request, 'entry/create_entry.html', context)
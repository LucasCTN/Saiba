# -*- coding: utf-8 -*-
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
#from .forms import AlbumForm, SongForm, UserForm
from .models import Entry, Revision, Category, EditorList
from .forms import EntryForm, RevisionForm
from django.utils.html import escape
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
from entry.serializers import EntrySerializer, RevisionSerializer
from gallery.models import Image, Video
import Saiba.saibadown, textile

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
    entry = get_object_or_404(Entry, slug=entry_slug)
    last_revision = Revision.objects.filter(entry=entry, hidden=False).latest('pk')
    first_revision = Revision.objects.filter(entry=entry, hidden=False).earliest('pk')
    last_images = Image.objects.filter(hidden=False).order_by('-id')[:10]
    last_videos = Video.objects.filter(hidden=False).order_by('-id')[:10]
    
    last_revision.content = Saiba.saibadown.parse(textile.textile(last_revision.content))
    editor_list = EditorList.objects.filter(entry=entry)

    args = {'entry': entry, 
            'last_revision':last_revision,                                                   
            'first_revision':first_revision, 
            'images':last_images,
            'videos':last_videos,
            'editor_list':editor_list,
            'type':'entry'}

    return render(request, 'entry/detail.html', args)

def history(request, entry_slug):
    entry = get_object_or_404(Entry, slug=entry_slug)
    revisions = Revision.objects.filter(entry=entry, hidden=False).order_by('-id')
    return render(request, escape('entry/history.html'), {'revisions': revisions, 'entry_name':entry.title, 'entry_slug':entry.slug})

def edit(request, entry_slug):
    if not request.user.is_authenticated():
        return redirect('home:login')
    else:
        user = request.user
        entry = Entry.objects.get(slug=entry_slug)
        last_revision = Revision.objects.filter(entry=entry, hidden=False).latest('pk')
        first_revision = Revision.objects.filter(entry=entry, hidden=False).earliest('pk')

        is_editor = EditorList.objects.filter(entry=entry, user=user)

        entry_form = EntryForm(request.POST or None, initial=model_to_dict(entry))
        revision_form = RevisionForm(request.POST or None, initial=model_to_dict(last_revision))

        if entry_form.is_valid() and revision_form.is_valid() and is_editor.exists():
            entry_form = EntryForm(request.POST, instance = entry)
            entry = entry_form.save(commit=False)
            entry.author = user
            entry.save()

            revision = revision_form.save(commit=False)
            revision.entry = entry
            revision.author = user
            revision.save()

            last_revision = Revision.objects.filter(entry=entry, hidden=False).latest('pk')
        
            last_images = Image.objects.filter(hidden=False).order_by('-id')[:10]
            return redirect('entry:detail', entry_slug=entry_slug)

        context = { "entry_form": entry_form, "revision_form": revision_form, "entry":entry, "user":user }

    return render(request, 'entry/edit.html', context)

def revision(request, entry_slug, revision_id):
    revision = get_object_or_404(Revision, hidden=False, pk=revision_id)
    return render(request, escape('entry/revision.html'), { 'revision': revision })

def create_entry(request):
    if not request.user.is_authenticated():
        return redirect('home:login')
    else:
        user = request.user
        entry_form = EntryForm(request.POST or None)
        revision_form = RevisionForm(request.POST or None)
        
        if entry_form.is_valid() and revision_form.is_valid():
            entry = entry_form.save(commit=False)
            entry.author = user
            entry.save()
            
            revision = revision_form.save(commit=False)
            revision.entry = entry
            revision.author = user
            revision.save()

            editorList = EditorList()
            editorList.user = user
            editorList.entry = entry
            editorList.save()

            last_revision = Revision.objects.filter(entry=entry, hidden=False).latest('pk')
            first_revision = Revision.objects.filter(entry=entry, hidden=False).earliest('pk')
            last_images = Image.objects.filter(hidden=False).order_by('-id')[:10]
            return render(request, 'entry/detail.html', {'entry': entry, 'last_revision':last_revision, 
                                                       'first_revision':first_revision, 'images':last_images})

        context = { "entry_form": entry_form, "revision_form": revision_form }

    return render(request, 'entry/create_entry.html', context)

def editorship(request, entry_slug):
    entry = get_object_or_404(Entry, slug=entry_slug)
    editor_list = EditorList.objects.filter(entry=entry)
    
    user_editor_list = list()
        
    for user_in_list in editor_list:
        user_editor_list.append(user_in_list.user)

    context = {'entry':entry, 'editor_list': editor_list, 'user_editor_list':user_editor_list}

    return render(request, 'entry/editorship.html', context)
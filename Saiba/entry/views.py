﻿    # -*- coding: utf-8 -*-
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Count, Max
#from .forms import AlbumForm, SongForm, UserForm
from .models import Entry, Revision, Category
from feedback.models import Comment
from .forms import EntryForm, RevisionForm
from django.utils.html import escape
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
from entry.serializers import EntrySerializer, RevisionSerializer
from gallery.models import Image, Video
from gallery.serializers import ImageSerializer
from home.models import SaibaSettings
import Saiba.saibadown, textile, ghdiff
from django.contrib.contenttypes.models import ContentType

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
    last_images = Image.objects.filter(hidden=False, entry=entry).order_by('-id')[:10]
    last_videos = Video.objects.filter(hidden=False, entry=entry).order_by('-id')[:10]
    
    related_entries = Entry.objects.filter(hidden=False, tags__in=entry.tags.all()).\
                        annotate(num_common_tags=Count('pk')).order_by('-num_common_tags').exclude(pk=entry.pk)[:5]

    last_revision.content = Saiba.saibadown.parse(textile.textile(last_revision.content))

    args = {'entry'             : entry, 
            'last_revision'     : last_revision,                                                   
            'first_revision'    : first_revision, 
            'images'            : last_images,
            'videos'            : last_videos,
            'related_entries'   : related_entries,
            'type'              : 'entry'}

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

        is_editor = user.profile in entry.editorship.all()

        entry_form = EntryForm(request.POST or None, request.FILES, initial=model_to_dict(entry))
        revision_form = RevisionForm(request.POST or None, initial=model_to_dict(last_revision))

        if entry_form.is_valid() and revision_form.is_valid() and is_editor:
            trending_weight = int(SaibaSettings.objects.get(type="trending_weight_entry_edit").value)
            entry.trending_points += trending_weight
            entry.save(update_fields=['trending_points'])
            
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
    previous_revision = Revision.objects.filter(entry=revision.entry.pk, hidden=False, pk__lt=revision_id).order_by('-id').first()

    revision_text = revision.content
    previous_revision_text = ""

    if previous_revision:
        previous_revision_text = previous_revision.content

    html_result = ghdiff.diff(previous_revision_text, revision_text)

    return render(request, escape('entry/revision.html'), { 'revision': revision, 'html': html_result })

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
            entry.editorship.add(user.profile)
            entry.save()
            
            revision = revision_form.save(commit=False)
            revision.entry = entry
            revision.author = user
            revision.save()

            last_revision = Revision.objects.filter(entry=entry, hidden=False).latest('pk')
            first_revision = Revision.objects.filter(entry=entry, hidden=False).earliest('pk')
            last_images = Image.objects.filter(hidden=False).order_by('-id')[:10]
            return render(request, 'entry/detail.html', {'entry': entry, 'last_revision':last_revision, 
                                                       'first_revision':first_revision, 'images':last_images})

        context = { "entry_form": entry_form,
                    "revision_form": revision_form }

    entry_form.fields['title'].widget.attrs['class'] = 'form-control form-title'
    entry_form.fields['category'].widget.attrs['class'] = 'form-control form-category'
    entry_form.fields['origin'].widget.attrs['class'] = 'form-control form-origin'
    entry_form.fields['additional_references'].widget.attrs['class'] = 'form-control form-additional_references'
    entry_form.fields['icon'].widget.attrs['class'] = 'form-control-file form-icon'
    revision_form.fields['content'].widget.attrs['class'] = 'form-control form-content'

    return render(request, 'entry/create_entry.html', context)

def editorship(request, entry_slug):
    entry = get_object_or_404(Entry, slug=entry_slug)
    editor_list = entry.editorship.all()
    
    user_editor_list = list()
        
    for user_in_list in editor_list:
        user_editor_list.append(user_in_list.user)

    context = {'entry':entry, 'editor_list': editor_list, 'user_editor_list':user_editor_list}

    return render(request, 'entry/editorship.html', context)

'''
    recently_revised_entries = Entry.objects.filter(hidden=False).annotate(num_revisions=Count('revisions')).order_by('-num_revisions')
    
    if not request.user.is_authenticated():
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
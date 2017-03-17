﻿    # -*- coding: utf-8 -*-
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import slugify
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
from home.models import SaibaSettings, Tag
import Saiba.saibadown, textile, ghdiff, Saiba.utils as utils
from django.contrib.contenttypes.models import ContentType

def index(request):
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

    trending_galleries  = utils.get_popular_galleries(request)
    trending_entries    = utils.get_trending_entries(request)

    args = {'entry'             : entry,
            'last_revision'     : last_revision,
            'first_revision'    : first_revision,
            'images'            : last_images,
            'videos'            : last_videos,
            'related_entries'   : related_entries,
            'type'              : 'entry',
            'trending_galleries': trending_galleries,
            'trending_entries'  : trending_entries }

    return render(request, 'entry/detail.html', args)

def history(request, entry_slug):
    trending_entries    = utils.get_trending_entries(request)
    entry = get_object_or_404(Entry, slug=entry_slug)
    revisions = Revision.objects.filter(entry=entry, hidden=False).order_by('-id')

    context = {'revisions'          : revisions, 
               'entry_name'         :entry.title, 
               'entry_slug'         :entry.slug,
               'trending_entries'   :trending_entries }

    return render(request, escape('entry/history.html'), context)

def edit(request, entry_slug):
    trending_entries    = utils.get_trending_entries(request)

    if not request.user.is_authenticated():
        return redirect('home:login')
    else:
        user = request.user
        entry = Entry.objects.get(slug=entry_slug)
        last_revision = Revision.objects.filter(entry=entry, hidden=False).latest('pk')
        first_revision = Revision.objects.filter(entry=entry, hidden=False).earliest('pk')

        is_editor = user.profile in entry.editorship.all()

        entry_form = EntryForm(request.POST or None, initial=model_to_dict(entry))
        revision_form = RevisionForm(request.POST or None, initial=model_to_dict(last_revision))

        if entry_form.is_valid() and revision_form.is_valid() and is_editor:
            all_tags = string_tags_to_list(request.POST.get('tags-selected'))
            set_tags = generate_tags(all_tags)

            trending_weight = int(SaibaSettings.objects.get(type="trending_weight_entry_edit").value)
            entry.trending_points += trending_weight
            entry.save(update_fields=['trending_points'])

            entry_form = EntryForm(request.POST, request.FILES, instance = entry)
            entry = entry_form.save(commit=False)
            entry.author = user
            entry.slug = slugify(entry.title)
            entry.save()
            entry_form.save_m2m()
            entry.tags = Tag.objects.filter(label__in=set_tags)
            entry.save()

            revision = revision_form.save(commit=False)
            revision.entry = entry
            revision.author = user
            revision.save()            

            return redirect('entry:detail', entry_slug=entry.slug)

        context = { "entry_form": entry_form, 
                   "revision_form": revision_form, 
                   "entry":entry, 
                   "user":user, 
                   'trending_entries':trending_entries }


    entry_form.fields['title'].widget.attrs['class'] = 'form-control form-title'
    entry_form.fields['category'].widget.attrs['class'] = 'form-control form-category'
    entry_form.fields['origin'].widget.attrs['class'] = 'form-control form-origin'
    entry_form.fields['date_origin'].widget.attrs['class'] = 'form-control form-date_origin'
    entry_form.fields['icon'].widget.attrs['class'] = 'form-control-file form-icon'
    revision_form.fields['content'].widget.attrs['class'] = 'form-control form-content'

    return render(request, 'entry/edit.html', context)

def revision(request, entry_slug, revision_id):
    trending_entries    = utils.get_trending_entries(request)
    revision = get_object_or_404(Revision, hidden=False, pk=revision_id)
    previous_revision = Revision.objects.filter(entry=revision.entry.pk, hidden=False, pk__lt=revision_id).order_by('-id').first()

    revision_text = revision.content
    previous_revision_text = ""

    if previous_revision:
        previous_revision_text = previous_revision.content

    html_result = ghdiff.diff(previous_revision_text, revision_text)

    return render(request, escape('entry/revision.html'), { 'revision': revision, 'html': html_result, 'trending_entries': trending_entries })

def create_entry(request):
    trending_entries    = utils.get_trending_entries(request)
    trending_gallery    = utils.get_popular_galleries(request)
    if not request.user.is_authenticated():
        return redirect('home:login')
    else:
        user = request.user
        entry_form = EntryForm(request.POST or None, request.FILES)
        revision_form = RevisionForm(request.POST or None)

        entry_test = Entry.objects.filter(slug=slugify(entry_form.fields['title'])).first()

        if entry_form.is_valid() and revision_form.is_valid() and not entry_test:
            all_tags = string_tags_to_list(request.POST.get('tags-selected'))
            set_tags = generate_tags(all_tags)
            
            print request.POST.get('tags-selected')

            entry = entry_form.save(commit=False)
            entry.author = user
            entry.save()
            entry.tags = Tag.objects.filter(label__in=set_tags)
            entry.editorship.add(user.profile)
            entry.save()
            
            revision = revision_form.save(commit=False)
            revision.entry = entry
            revision.author = user
            revision.save()

            last_revision = Revision.objects.filter(entry=entry, hidden=False).latest('pk')
            first_revision = Revision.objects.filter(entry=entry, hidden=False).earliest('pk')
            last_images = Image.objects.filter(hidden=False).order_by('-id')[:10]
            return redirect('entry:detail', entry_slug=entry.slug)

        context = { "entry_form"        : entry_form,
                    "revision_form"     : revision_form,
                    "trending_entries"  : trending_entries,
                    "trending_gallery"  : trending_gallery }

    entry_form.fields['title'].widget.attrs['class'] = 'form-control form-title'
    entry_form.fields['category'].widget.attrs['class'] = 'form-control form-category'
    entry_form.fields['origin'].widget.attrs['class'] = 'form-control form-origin'
    entry_form.fields['date_origin'].widget.attrs['class'] = 'form-control form-date_origin'
    entry_form.fields['icon'].widget.attrs['class'] = 'form-control-file form-icon'
    revision_form.fields['content'].widget.attrs['class'] = 'form-control form-content'

    return render(request, 'entry/create_entry.html', context)

def editorship(request, entry_slug):
    trending_entries    = utils.get_trending_entries(request)
    entry = get_object_or_404(Entry, slug=entry_slug)
    editor_list = entry.editorship.all()
    
    user_editor_list = list()
        
    for user_in_list in editor_list:
        user_editor_list.append(user_in_list.user)

    context = {'entry':entry, 'editor_list': editor_list, 'user_editor_list':user_editor_list, 'trending_entries':trending_entries}
    return render(request, 'entry/editorship.html', context)

def manage_editorship(request, entry_slug):
    trending_entries    = utils.get_trending_entries(request)
    trending_gallery    = utils.get_popular_galleries(request)

    if not request.user.is_staff:
        return redirect('home:index')

    entry = Entry.objects.get(slug=entry_slug)
    editor = None

    if ('editor_name' in request.POST) and (request.POST['editor_name'] is not None) and request.POST['editor_name']:
        editor_name = request.POST['editor_name'] #sanitize this
        editor = Profile.objects.get(user__username=editor_name)
        entry.editorship.add(editor)

    if 'remove_editor' in request.POST:
        editor_name = request.POST['remove_editor'] #sanitize this
        editor = Profile.objects.get(user__username=editor_name)
        entry.editorship.remove(editor)

    context = { 'entry': entry, 'trending_entries': trending_entries, 'trending_gallery': trending_gallery }
   
    return render(request, 'entry/manage_editorship.html', context)

def string_tags_to_list( tag_string ):
    if(tag_string != None):
        # Splitting all commas
        tags = tag_string.split(",")
        # Removing empty spaces
        tags[:] = (value for value in tags if value != '')
        # Removing all duplicates and returning it (the insertion order it's lost unfortunately)
        return list(set(tags))
    else:
        return ''

def generate_tags( tag_list ):
    # Of the tags written, which one is in database
    db_tags = Tag.objects.filter(label__in=tag_list)

    # Creating a copy of the all tag list
    new_tags = list(tag_list)

    # Removing database tag from the new list (if have any)
    for x in db_tags:
        new_tags[:] = (value for value in new_tags if value != str(x).decode("utf-8"))

    # Inserting in database the new tags
    for tag_name in new_tags:
        Tag.objects.create(label=tag_name, hidden=False)

    # Returning a new list with the database tags and the new created tags
    return list(db_tags) + new_tags

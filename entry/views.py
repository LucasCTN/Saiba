﻿# -*- coding: utf-8 -*-
import urllib
from profile.models import Profile

import ghdiff
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template.defaultfilters import slugify
from django.utils.html import escape

import saiba
from feedback.models import TrendingVote, View
from gallery.models import Image, Video
from home.models import SaibaSettings, Tag

from .forms import EntryForm, RevisionForm, StaffEntryForm
from .models import Entry, EntryRedirect, Revision


def index(request):
    '''An "invalid" page that will redirect the user to a search page.'''
    return HttpResponseRedirect("%s?%s" % (reverse('home:page_search'),
                                           urllib.urlencode({"tipo": "entrada"})))

def detail(request, entry_slug):
    entry_redirect = EntryRedirect.objects.filter(slug=entry_slug).first()

    if entry_redirect:
        redirect_slug = str(entry_redirect.entry.slug)
        return redirect('entry:detail', entry_slug=redirect_slug)

    entry = get_object_or_404(Entry, slug=entry_slug)

    if entry.hidden and not request.user.is_staff:
        return redirect('home:index')

    last_revision = Revision.objects.filter(entry=entry, hidden=False).latest('pk')
    first_revision = Revision.objects.filter(entry=entry, hidden=False).earliest('pk')
    last_images = Image.objects.filter(hidden=False, entry=entry).order_by('-id')[:10]
    last_videos = Video.objects.filter(hidden=False, entry=entry).order_by('-id')[:10]

    saiba.utils.register_view(request, entry)

    related_entries = Entry.objects.filter(hidden=False, tags__in=entry.tags.all()).\
                        annotate(num_common_tags=Count('pk')).order_by('-num_common_tags').exclude(pk=entry.pk)[:5]

    if request.user.is_authenticated():
        can_see_editorship = entry.editorship.filter(user=request.user).exists() or request.user.profile.HasPermission('edit_entry')
    else:
        can_see_editorship = False

    last_revision.content = saiba.parser.parse(last_revision.content)

    trending_galleries  = saiba.utils.get_popular_galleries(request)

    can_lock_gallery = False
    if request.user.is_authenticated():
        can_lock_gallery = request.user.profile.HasPermission('lock_gallery')        

    if request.user.is_authenticated():
        can_lock_gallery = request.user.profile.HasPermission('lock_gallery')

    type = ContentType.objects.get_for_model(Entry)
    views = View.objects.filter(target_content_type=type, target_id=entry.id).count()

    args = {'entry'             : entry,
            'id'                : entry.id,
            'type'              : 'entry',
            'last_revision'     : last_revision,
            'first_revision'    : first_revision,
            'images'            : last_images,
            'videos'            : last_videos,
            'related_entries'   : related_entries,
            'trending_galleries': trending_galleries,
            'can_see_editorship': can_see_editorship,
            'can_lock_gallery'  : can_lock_gallery,
            'target'            : entry,
            'views'             : views }

    return render(request, 'entry/detail.html', args)

def history(request, entry_slug):
    entry = get_object_or_404(Entry, slug=entry_slug)
    revisions = Revision.objects.filter(entry=entry, hidden=False).order_by('-id')

    context = {'revisions'  : revisions, 
               'entry_name' : entry.title, 
               'entry_slug' : entry.slug }

    return render(request, escape('entry/history.html'), context)

@login_required
def edit(request, entry_slug):
    user = request.user
    entry = Entry.objects.get(slug=entry_slug)
    redirects = EntryRedirect.objects.filter(entry=entry)

    last_revision = Revision.objects.filter(entry=entry, hidden=False).latest('pk')
    first_revision = Revision.objects.filter(entry=entry, hidden=False).earliest('pk')

    is_editor = user.profile in entry.editorship.all()

    revision_form = RevisionForm(request.POST or None, initial=model_to_dict(last_revision))

    if request.user.profile.HasPermission('lock_gallery'):
        entry_form = StaffEntryForm(request.POST or None, request.FILES or None, initial=model_to_dict(entry), instance=entry)
    else:
        entry_form = EntryForm(request.POST or None, request.FILES or None, initial=model_to_dict(entry), instance=entry)

    if entry_form.is_valid() and revision_form.is_valid() and is_editor:
        all_tags = saiba.utils.string_tags_to_list(request.POST.get('tags-selected'))
        set_tags = saiba.utils.generate_tags(all_tags, Tag)

        trending_weight = int(SaibaSettings.objects.get(type="trending_weight_entry_edit").value)
        entry.trending_points += trending_weight
        entry.save(update_fields=['trending_points'])

        entry = entry_form.save(commit=False)
        entry.author = user
        entry.slug = slugify(entry.title)
        entry.save()
        entry_form.save_m2m()
        entry.tags = Tag.objects.filter(label__in=set_tags)
        entry.create_action("6")
        entry.save()

        vote_type_model = SaibaSettings.objects.get(type='trending_weight_entry_edit')
        trending_vote = TrendingVote.objects.create(author=request.user, entry=entry,
                                                    vote_type=vote_type_model)

        revision = revision_form.save(commit=False)
        revision.entry = entry
        revision.author = user
        revision.save()

        return redirect('entry:detail', entry_slug=entry.slug)

    context = { "entry_form"        : entry_form,
                "revision_form"     : revision_form,
                "entry"             : entry,
                "user"              : user,
                "redirects"         : redirects}

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

@login_required
def create_entry(request):
    trending_gallery = saiba.utils.get_popular_galleries(request)

    user = request.user
    entry_form = EntryForm(request.POST or None, request.FILES)
    revision_form = RevisionForm(request.POST or None)

    entry_duplicate_title = Entry.objects.filter(slug=slugify(request.POST.get('title'))).first()

    errors = {}

    if(request.POST):
        for error in entry_form.errors:
            errors[error] = entry_form.errors[error].as_text

        for error in revision_form.errors:
            errors[error] = revision_form.errors[error].as_text

    if entry_form.is_valid() and revision_form.is_valid() and entry_duplicate_title == None:
        entry = entry_form.save(commit=False)

        all_tags = saiba.utils.string_tags_to_list(request.POST.get('tags-selected'))
        set_tags = saiba.utils.generate_tags(all_tags, Tag)

        date_origin = saiba.utils.verify_and_format_date(request.POST.get('date-day'), request.POST.get('date-month'), request.POST.get('date-year'))

        if date_origin != False:
            entry.date_origin = date_origin
            entry.save()
            entry.tags = Tag.objects.filter(label__in=set_tags)
            entry.editorship.add(user.profile)
            entry.create_action("3")
            entry.save()

            revision = revision_form.save(commit=False)
            revision.entry = entry
            revision.author = user
            revision.save()

            last_revision = Revision.objects.filter(entry=entry, hidden=False).latest('pk')
            first_revision = Revision.objects.filter(entry=entry, hidden=False).earliest('pk')
            last_images = Image.objects.filter(hidden=False).order_by('-id')[:10]

            return redirect('entry:detail', entry_slug=entry.slug)
        else:
            errors['date_origin'] = saiba.custom_messages.get_custom_error_message('invalid_date')

    elif entry_duplicate_title != None:
        errors['title'] = saiba.custom_messages.get_custom_error_message('duplicated_entry')

    context =  {"entry_form"        : entry_form,
                "revision_form"     : revision_form,
                "trending_gallery"  : trending_gallery,
                "error_messages"    : errors}

    return render(request, 'entry/create_entry.html', context)

def editorship(request, entry_slug):
    entry = get_object_or_404(Entry, slug=entry_slug)
    editor_list = entry.editorship.all()
    
    user_editor_list = list()
        
    for user_in_list in editor_list:
        user_editor_list.append(user_in_list.user)

    context = {'entry':entry, 'editor_list': editor_list, 'user_editor_list':user_editor_list}

    return render(request, 'entry/editorship.html', context)

def manage_editorship(request, entry_slug):
    entry = Entry.objects.get(slug=entry_slug)
    has_full_rights = request.user == entry.author or request.user.profile.HasPermission('edit_entry')

    if not has_full_rights and not entry.editorship.filter(user=request.user).exists():
        return redirect('entry:detail', entry_slug=entry_slug)

    editor_added = request.POST.get('editor_added')
    editor_removed = request.POST.get('editor_removed')

    entry = Entry.objects.get(slug=entry_slug)

    if editor_added:
        editor = Profile.objects.get(slug=editor_added)
        entry.editorship.add(editor)

    if editor_removed:
        editor = Profile.objects.get(slug=editor_removed)
        if editor.user == request.user or has_full_rights:
            entry.editorship.remove(editor)

    context = {'entry': entry, 'has_full_rights': has_full_rights}

    return render(request, 'entry/manage_editorship.html', context)

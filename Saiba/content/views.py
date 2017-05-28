# -*- coding: utf-8 -*-
from django.contrib.admin.views.decorators import staff_member_required
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404, redirect, render
from django.template.defaultfilters import slugify

from home.models import Tag
from Saiba import utils, parser

from .forms import BPostForm
from .models import BPost


def bpost_detail(request, bpost_slug):
    '''Page for detailing a BPost.'''
    bpost = get_object_or_404(BPost.objects.active(), slug=bpost_slug)
    bpost.content = parser.parse(bpost.content)

    context = {'content': bpost, 'content_type': 'bpost'} # For compatilibity with comment sections
    return render(request, 'content/content_detail.html', context)


@staff_member_required
def bpost_edit(request, bpost_slug):
    '''Page for editing an existing BPost.'''
    bpost = get_object_or_404(BPost.objects.active(), slug=bpost_slug)
    bpost_form = BPostForm(request.POST or None, request.FILES or None, initial=model_to_dict(bpost), instance=bpost)

    if bpost_form.is_valid():
        all_tags = utils.string_tags_to_list(request.POST.get('tags-selected'))
        set_tags = utils.generate_tags(all_tags, Tag)

        bpost = bpost_form.save(commit=False)
        bpost.author = request.user
        bpost.slug = slugify(bpost.title)
        bpost.save()
        bpost_form.save_m2m()
        bpost.tags = Tag.objects.filter(label__in=set_tags)
        bpost.save()

    context = {'content': bpost, 'content_type': 'bpost', 'form': bpost_form}
    return render(request, 'content/content_edit.html', context)

@staff_member_required
def bpost_create(request):
    '''Page for creating a new BPost.'''
    bpost_form = BPostForm(request.POST or None, request.FILES)

    if bpost_form.is_valid():
        all_tags = utils.string_tags_to_list(request.POST.get('tags-selected'))
        set_tags = utils.generate_tags(all_tags, Tag)

        bpost = bpost_form.save()
        bpost.tags = Tag.objects.filter(label__in=set_tags)
        bpost.save()
        return redirect('content:bpost_detail', bpost_slug=bpost.slug)

    context = {'form': bpost_form}
    return render(request, 'content/content_create.html', context)

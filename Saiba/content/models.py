# -*- coding: utf-8 -*-
import datetime

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.template.defaultfilters import slugify

from .managers import BPostManager


class Content(models.Model):
    '''Basic model for the content app. It should be inherited from the other models.'''
    author = models.ForeignKey(User, default=1)
    comments_locked = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    hidden = models.BooleanField(default=False)
    icon = models.ImageField(upload_to='icon/', blank=True)
    icon_url = models.URLField(blank=True)
    title = models.CharField(max_length=250)
    view = GenericRelation('feedback.View')
    slug = models.SlugField(max_length=250, default="", blank=True, unique=True)
    tags = models.ManyToManyField('home.Tag', blank=True)
    update_date = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name_plural = "contents"

class BPostCategory(models.Model):
    '''Model for categorizing only Blog Post objects.'''
    description = models.CharField(max_length=2500, blank=True)
    label = models.CharField(max_length=2500)

    def __unicode__(self):
        return self.label

    class Meta:
        verbose_name_plural = "BPost categories"

class BPost(Content):
    '''Blog Post model, for staff-made posts that aren't in frontpage.'''
    category = models.ForeignKey(BPostCategory, blank=True, null=True)
    content = models.CharField(max_length=2500, blank=True) # The post's textual content

    objects = BPostManager()

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id: # Is a new post
            self.slug = slugify(self.title) # Generating a slug on creation
        super(BPost, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "BPosts"

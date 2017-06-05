# -*- coding: utf-8 -*-
import datetime

from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.fields import GenericRelation
from django.core.files.base import ContentFile
from django.db import models
from django.template.defaultfilters import slugify

import saiba.image_utils
from feedback.models import Action

class Status(models.Model):
    label = models.CharField(max_length=2500, blank=True)
    code_name = models.CharField(max_length=2500, blank=True)
    description = models.CharField(max_length=2500, blank=True)

    def __unicode__(self):
        return self.label

    class Meta:
        verbose_name_plural = "status"

class Category(models.Model):
    label = models.CharField(max_length=2500, blank=True)
    description = models.CharField(max_length=2500, blank=True)

    def __unicode__(self):
        return self.label

    class Meta:
        verbose_name_plural = "categories"

class Entry(models.Model):
    author                  = models.ForeignKey(User, default=1)
    title                   = models.CharField(max_length=250)
    slug                    = models.SlugField(max_length=250, default="", blank=True, unique=True, db_index=True)
    status                  = models.ForeignKey(Status, default=1)
    category                = models.ForeignKey(Category, default=1)
    type                    = models.CharField(max_length=100, blank=True)
    date_origin             = models.CharField(max_length=100, blank=True)
    origin                  = models.CharField(max_length=100)
    icon                    = models.ImageField(upload_to='icon/', blank=True)
    icon_url                = models.URLField(blank=True)
    hidden                  = models.BooleanField(default=False)
    images_locked           = models.BooleanField(default=False)
    videos_locked           = models.BooleanField(default=False)
    comments_locked         = models.BooleanField(default=False)
    tags                    = models.ManyToManyField('home.Tag', blank=True)
    trending_points         = models.IntegerField(default=0)
    editorship              = models.ManyToManyField('profile.Profile', blank=True)
    view                    = GenericRelation('feedback.View')

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        if self.icon_url and not self.icon:
            image_name, image_content = saiba.image_utils.download_external_image(self.icon_url)
            
            if image_name and image_content != None:
                self.icon.save(image_name, ContentFile(image_content), save=False)

        super(Entry, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    def create_action(self, action_type_number = "0"):
        new_action = Action.objects.create(author=self.author, target=self, target_id=self.id, action_type=action_type_number)
        new_action.save()

    class Meta:
        verbose_name_plural = "entries"
        index_together = ( ('id', 'slug'), )

class Revision(models.Model):
    author = models.ForeignKey(User, default=1)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name="revisions")
    content = models.TextField(max_length=2500)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    hidden = models.BooleanField(default=False)

    def __unicode__(self):
        return "#{} - {}".format(str(self.pk), self.entry.title)

class EntryRedirect(models.Model):
    entry = models.ForeignKey(Entry, default=1)
    slug = models.SlugField(max_length=250, default="", blank=True, unique=True)

    def __unicode__(self):
        return self.slug + " (" + self.entry.title + ")"

import os
import urllib2

from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.fields import GenericRelation
from django.core.files.base import ContentFile
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.contrib.contenttypes.fields import GenericRelation

import Saiba.image_utils
from feedback.models import Action
from home.models import SaibaSettings


class State(models.Model):
    label       = models.CharField(max_length=250)
    description = models.CharField(max_length=250)

    def __unicode__(self):
        return self.label

class Image(models.Model):
    author          = models.ForeignKey(User, blank=True)
    title           = models.CharField(max_length=250)
    date            = models.DateTimeField(default=timezone.now, blank=True)
    date_origin     = models.CharField(max_length=100, blank=True)
    source          = models.CharField(max_length=250)
    tags            = models.ManyToManyField('home.Tag', blank=True)
    entry           = models.ForeignKey('entry.Entry', on_delete=models.CASCADE, related_name="images")
    hidden          = models.BooleanField(default=False)
    file            = models.ImageField(upload_to='icon/', blank=True)
    file_url        = models.URLField(blank=True)
    description     = models.TextField(max_length=250, blank=True)
    state           = models.ForeignKey(State, on_delete=models.CASCADE, default=1)
    trending_points = models.IntegerField(default=0)
    views           = GenericRelation('feedback.View')
    votes = GenericRelation('feedback.TrendingVote', related_query_name='images')

    def __unicode__(self):
        return self.entry.title + ' - ' + self.title

    def create_action(self, action_type_number = "0"):
        new_action = Action.objects.create(author=self.author, target=self, target_id=self.id, action_type=action_type_number)
        new_action.save()

    def increase_trending_points(self, criteria=""):
        trending_weight = int(SaibaSettings.objects.get(type=criteria).value)
        self.trending_points += trending_weight
        self.save()
    
    def save(self, *args, **kwargs):        
        if self.file_url and not self.file:
            image_name, image_content = Saiba.image_utils.download_external_image(self.file_url)
            self.file.save(image_name, ContentFile(image_content), save=False)
        super(Image, self).save(*args, **kwargs)

class Video(models.Model):
    author          = models.ForeignKey(User, blank=True)
    title           = models.CharField(max_length=250)
    date            = models.DateTimeField(default=timezone.now, blank=True)
    date_origin     = models.CharField(max_length=100, blank=True)
    tags            = models.ManyToManyField('home.Tag', blank=True)
    entry           = models.ForeignKey('entry.Entry', on_delete=models.CASCADE)
    hidden          = models.BooleanField(default=False)
    link            = models.CharField(max_length=250)
    description     = models.TextField(max_length=250, blank=True)
    state           = models.ForeignKey(State, on_delete=models.CASCADE, default=1)
    trending_points = models.IntegerField(default=0)
    views           = GenericRelation('feedback.View')
    votes = GenericRelation('feedback.TrendingVote', related_query_name='videos')

    def __unicode__(self):
        return self.entry.title + ' - ' + self.title

    def create_action(self, action_type_number = "0"):
        new_action = Action.objects.create(author=self.author, target=self, target_id=self.id, action_type=action_type_number)
        new_action.save()

    def increase_trending_points(self, criteria=""):
        trending_weight = int(SaibaSettings.objects.get(type=criteria).value)
        self.trending_points += trending_weight
        self.save()

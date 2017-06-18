# -*- coding: utf-8 -*-
import datetime
import time

from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.contrib.sessions.models import Session

from home.models import SaibaSettings

class Vote(models.Model):
    target_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    target_id           = models.PositiveIntegerField(null=True, blank=True)
    target              = GenericForeignKey('target_content_type', 'target_id')
    author              = models.ForeignKey(User)
    creation_date       = models.DateTimeField(auto_now_add=True, blank=True)
    update_date         = models.DateTimeField(auto_now=True, blank=True)
    direction           = models.IntegerField(default=0)

    def __str__(self):
        text = "#{} - {}".format(self.id, self.author.username)
        return text

class Comment(models.Model):
    target_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    target_id           = models.PositiveIntegerField(null=True, blank=True)
    target              = GenericForeignKey('target_content_type', 'target_id')
    author              = models.ForeignKey(User)
    content             = models.CharField(max_length=250)
    creation_date       = models.DateTimeField(auto_now_add=True, blank=True)
    update_date         = models.DateTimeField(auto_now=True, blank=True)
    hidden              = models.BooleanField(default=False)
    is_deleted          = models.BooleanField(default=False)
    parent              = models.ForeignKey('feedback.Comment', on_delete=models.CASCADE, null=True, blank=True, 
                                            related_name="children") # for tracking the main comment when replying a reply
    reply_to            = models.ForeignKey('feedback.Comment', on_delete=models.CASCADE, null=True, blank=True, 
                                            related_name="replies") # the immediate response (may not be the main comment)
    points              = models.IntegerField(default=0)

    def __str__(self):
        text = "#{} - {}".format(self.id, self.author.username)
        if self.parent: 
            text += " (child of #{})".format(self.parent.id)
        return text

    def get_points(self):
        content_type = ContentType.objects.get_for_model(Comment)
        points = Vote.objects.filter(target_id=self.id, target_content_type=content_type).aggregate(Sum('direction'))['direction__sum']
        return points or 0

    def should_limit_child(self, id, limit):
        if self.id == id:
            return ""
        else:
            return limit

    def save(self, *args, **kwargs):
        super(Comment, self).save(*args, **kwargs)

    def update_points(self):
        self.points = self.get_points()
        self.save()

    def create_action(self, action_type_number = "0"):
        new_action = Action.objects.create(author=self.author, target=self, target_id=self.id, action_type=action_type_number)
        new_action.save()

# Class used for the activity system
class Action(models.Model):
    ACTION_TYPE_CHOICES = (
        ("0", "Unknown"),
        ("1", "New comment"),
        ("2", "New reply"),
        ("3", "New entry"),
        ("4", "New image"),
        ("5", "New video"),
        ("6", "Edit entry"),
        ("7", "Edit image"),
        ("8", "Edit video"),
    )

    target_content_type     = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    target_id               = models.PositiveIntegerField(null=True, blank=True)
    target                  = GenericForeignKey('target_content_type', 'target_id')
    author                  = models.ForeignKey(User)
    action_type             = models.CharField(
        max_length=1,
        choices=ACTION_TYPE_CHOICES,
        default="0",
    )
    date                = models.DateTimeField(auto_now_add=True, blank=True)
    is_public           = models.BooleanField(default=True)
    is_staff_only       = models.BooleanField(default=False)

    def __str__(self):
        text = "#{} by {} (Operation: {})".format(self.id, self.author.username, self.action_type)
        return text

class View(models.Model):
    author              = models.ForeignKey(User, blank=True, null=True)
    ip                  = models.GenericIPAddressField()
    user_agent          = models.CharField(max_length=200)
    target_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    target_id           = models.PositiveIntegerField(null=True, blank=True)
    target              = GenericForeignKey('target_content_type', 'target_id')
    date                = models.DateTimeField(auto_now_add=True, blank=True)
    session             = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        if self.author:
            name = self.author.username
        else:
            name = "Anonymous"

        return "#" + str(self.id) + " - [" + str(self.target_content_type) + "] " + self.target.title + " por " + name

class TrendingVote(models.Model):
    author              = models.ForeignKey(User)
    vote_type           = models.ForeignKey(SaibaSettings)
    creation_date       = models.DateTimeField(auto_now_add=True, blank=True)
    is_deleted          = models.BooleanField(default=False)
    points              = models.FloatField(default=0)
    entry               = models.ForeignKey('entry.Entry', related_name="trending_votes", blank=True, null=True)
    image               = models.ForeignKey('gallery.Image', related_name="trending_votes", blank=True, null=True)
    video               = models.ForeignKey('gallery.Video', related_name="trending_votes", blank=True, null=True)

    def __str__(self):
        text = "#{} by {}".format(self.id, self.author.username)        
        return text
    
    def set_points(self):
        vote_value = self.vote_type.value
        time_weight = SaibaSettings.objects.get(type="trending_weight_time").value
        seconds = time.mktime(datetime.datetime.now().timetuple())

        self.points = vote_value + (time_weight * seconds)

    def save(self, *args, **kwargs):
        self.set_points()
        super(TrendingVote, self).save(*args, **kwargs)

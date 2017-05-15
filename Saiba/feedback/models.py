# -*- coding: utf-8 -*-
from django.db.models import Sum
from django.contrib.auth.models import Permission, User
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone

class Vote(models.Model):
    target_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    target_id           = models.PositiveIntegerField(null=True, blank=True)
    target              = GenericForeignKey('target_content_type', 'target_id')
    author              = models.ForeignKey(User)
    creation_date       = models.DateTimeField(auto_now_add=True, blank=True)
    update_date         = models.DateTimeField(auto_now=True, blank=True)
    direction           = models.IntegerField(default=0)

    def __unicode__(self):
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

    def __unicode__(self):
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
    
    def __unicode__(self):
        text = "#{} by {} (Operation: {})".format(self.id, self.author.username, self.action_type)
        return text

class TrendingVote(models.Model):
    entry               = models.ForeignKey('entry.Entry')
    author              = models.ForeignKey(User)
    vote_type           = models.ForeignKey('home.SaibaSettings')   
    creation_date       = models.DateTimeField(auto_now_add=True, blank=True)
    is_deleted          = models.BooleanField(default=False)    
    points              = models.IntegerField(default=0)

    def __unicode__(self):
        text = "#{} by {}".format(self.id, self.author.username)        
        return text

    def get_points(self):
        content_type = ContentType.objects.get_for_model(Comment)
        points = Vote.objects.filter(target_id=self.id, target_content_type=content_type).aggregate(Sum('direction'))['direction__sum']
        return points or 0

    def trending_calculation(self):
        return trending_list

    def save(self, *args, **kwargs):
        super(Comment, self).save(*args, **kwargs)
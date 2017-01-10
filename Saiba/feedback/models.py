from django.contrib.auth.models import Permission, User
from django.db import models
from entry.models import Entry
from gallery.models import Image, Video
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone

class Vote(models.Model):
    target_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    target_id           = models.PositiveIntegerField(null=True, blank=True)
    target              = GenericForeignKey('target_content_type', 'target_id')
    author              = models.ForeignKey(User, default=1)
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
    author              = models.ForeignKey(User, default=1)
    content             = models.CharField(max_length=250)
    creation_date       = models.DateTimeField(auto_now_add=True, blank=True)
    update_date         = models.DateTimeField(auto_now=True, blank=True)
    hidden              = models.BooleanField(default=False)
    is_deleted          = models.BooleanField(default=False)

    def __unicode__(self):
        text = "#{} - {}".format(self.id, self.author.username)
        return text

class Reply(models.Model):    
    author          = models.ForeignKey(User, default=1)
    content         = models.CharField(max_length=250)
    creation_date   = models.DateTimeField(auto_now_add=True, blank=True)
    update_date     = models.DateTimeField(auto_now=True, blank=True)
    comment         = models.ForeignKey(Comment, default=None, blank=True, null=True, related_name="replies")
    response_to     = models.ForeignKey('self', default=None, blank=True, null=True, related_name="responses")
    hidden          = models.BooleanField(default=False)
    is_deleted      = models.BooleanField(default=False)

    def __unicode__(self):
        text = "#{} - {}".format(self.id, self.author.username)
        return text

    class Meta:
        verbose_name_plural = "replies"
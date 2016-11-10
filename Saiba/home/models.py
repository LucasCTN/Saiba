from django.db import models
from django.contrib.auth.models import Permission, User
from entry.models import Entry
from gallery.models import Image, Video
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Label(models.Model):
    name        = models.CharField(max_length=2500, blank=True)
    description = models.CharField(max_length=2500, blank=True)
    color       = models.CharField(max_length=300, blank=True)
    icon        = models.ImageField(blank=True, upload_to='label/')

    def __unicode__(self):
        return "[" + self.color + "] " + self.name

class Post(models.Model):
    author      = models.ForeignKey(User, default=1)
    label       = models.ForeignKey(Label, blank=True)
    title       = models.CharField(max_length=250)
    content     = models.TextField(max_length=2500, blank=True)
    hidden      = models.BooleanField(default=False)
    date        = models.DateTimeField(auto_now_add=True, blank=True)
    entry       = models.ForeignKey(Entry, blank=True, null=True)
    image       = models.ForeignKey(Image, blank=True, null=True)
    video       = models.ForeignKey(Video, blank=True, null=True)
    fixed       = models.BooleanField(default=False)

    def __unicode__(self):
        if(self.fixed):
            return "[Fixed] " + self.title
        else:
            return self.title

class Tag(models.Model):
    label   = models.CharField(max_length=2500, blank=True)
    hidden  = models.BooleanField(default=False)

    def __unicode__(self):
        return self.label
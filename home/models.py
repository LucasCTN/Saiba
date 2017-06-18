from django.db import models
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Label(models.Model):
    name        = models.CharField(max_length=2500, blank=True)
    description = models.CharField(max_length=2500, blank=True)
    color       = models.CharField(max_length=300, blank=False)
    icon        = models.ImageField(blank=True, upload_to='label/')

    def __str__(self):
        return "[ {} ] {}".format(self.color, self.name)

class Post(models.Model):
    author      = models.ForeignKey(User, default=1)
    label       = models.ForeignKey(Label, blank=True, null=True)
    title       = models.CharField(max_length=250)
    content     = models.TextField(max_length=2500, blank=True)
    hidden      = models.BooleanField(default=False)
    date        = models.DateTimeField(auto_now_add=True, blank=True)
    entry       = models.ForeignKey('entry.Entry', blank=True, null=True)
    image       = models.ForeignKey('gallery.Image', blank=True, null=True)
    video       = models.ForeignKey('gallery.Video', blank=True, null=True)
    fixed       = models.BooleanField(default=False)

    def __str__(self):
        if(self.fixed):
            return "[Fixed] " + self.title
        else:
            return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        if self.entry:
            return self.entry.get_absolute_url()
        elif self.image:
            return self.image.get_absolute_url()
        elif self.video:
            return self.video.get_absolute_url()

class Tag(models.Model):
    label   = models.CharField(max_length=2500, blank=True)
    hidden  = models.BooleanField(default=False)

    def __str__(self):
        return self.label

class SaibaSettings(models.Model):
    value = models.FloatField()
    type  = models.CharField(unique=True, max_length=300)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name_plural = "Saiba settings"
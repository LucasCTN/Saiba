from django.contrib.auth.models import Permission, User
from django.template.defaultfilters import slugify
from django.db import models
import datetime
from django.contrib.contenttypes.fields import GenericRelation

class Status(models.Model):
    label = models.CharField(max_length=2500, blank=True)
    description = models.CharField(max_length=2500, blank=True)

    def __unicode__(self):
        return self.label

class Category(models.Model):
    label = models.CharField(max_length=2500, blank=True)
    description = models.CharField(max_length=2500, blank=True)

    def __unicode__(self):
        return self.label

    class Meta:
        verbose_name_plural = "comentaries"

class Entry(models.Model):
    author                  = models.ForeignKey(User, default=1)
    title                   = models.CharField(max_length=250)
    slug                    = models.SlugField(max_length=250, default="", blank=True)
    status                  = models.ForeignKey(Status, default=1)
    category                = models.ForeignKey(Category, default=1)
    type                    = models.CharField(max_length=100, blank=True)
    date_origin             = models.CharField(max_length=100, blank=True)
    origin                  = models.CharField(max_length=100)
    icon                    = models.ImageField(blank=True, upload_to='icon/')
    hidden                  = models.BooleanField(default=False)
    images_locked           = models.BooleanField(default=False)
    videos_locked           = models.BooleanField(default=False)
    comments_locked         = models.BooleanField(default=False)
    tags                    = models.ManyToManyField('home.Tag', blank=True)
    trending_points         = models.IntegerField(default=0)
    editorship              = models.ManyToManyField('profile.Profile', blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.title)
        super(Entry, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name_plural = "entries"

class Revision(models.Model):
    author = models.ForeignKey(User, default=1)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name="revisions")
    content = models.TextField(max_length=2500)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    hidden = models.BooleanField(default=False)

    def __unicode__(self):
        return "#{} - {}".format(str(self.pk), self.entry.title)
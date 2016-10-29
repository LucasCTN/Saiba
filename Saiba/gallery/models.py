from django.contrib.auth.models import Permission, User
from django.db import models
import datetime
from entry.models import Entry

class State(models.Model):
    label       = models.CharField(max_length=250)
    description = models.CharField(max_length=250)

    def __unicode__(self):
        return self.label

class Image(models.Model):
    author = models.ForeignKey(User, blank=True)
    title = models.CharField(max_length=250)
    date = models.DateTimeField(default=datetime.datetime.now, blank=True)
    source = models.CharField(max_length=250)
    tags = models.CharField(max_length=250)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    hidden = models.BooleanField(default=False)
    file = models.ImageField(blank=True, upload_to='icon/')
    description = models.CharField(max_length=250, blank=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, default=1)

    def __unicode__(self):
        return self.entry.title + ' - ' + self.title

class Video(models.Model):
    author = models.ForeignKey(User, blank=True)
    title = models.CharField(max_length=250)
    date = models.DateTimeField(default=datetime.datetime.now, blank=True)
    tags = models.CharField(max_length=250)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    hidden = models.BooleanField(default=False)
    link = models.CharField(max_length=250)
    description = models.CharField(max_length=250, blank=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, default=1)

    def __unicode__(self):
        return self.entry.title + ' - ' + self.title
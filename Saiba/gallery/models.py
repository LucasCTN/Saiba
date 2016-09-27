from django.contrib.auth.models import Permission, User
from django.db import models
import datetime
from entry.models import Entry

class Image(models.Model):
    author = models.ForeignKey(User, default=1)
    title = models.CharField(max_length=250)
    date = models.DateTimeField(default=datetime.datetime.now, blank=True)
    source = models.CharField(max_length=250)
    tags = models.CharField(max_length=250)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    hidden = models.BooleanField(default=False)
    file = models.ImageField(blank=True)

    def __unicode__(self):
        return self.title + ' - ' + self.entry.title
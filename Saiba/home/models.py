from django.db import models
from django.contrib.auth.models import Permission, User
from entry.models import Entry, Category
from gallery.models import Image, Video

class Post(models.Model):
    author      = models.ForeignKey(User, default=1)
    category    = models.ForeignKey(Category, default=1)
    title       = models.CharField(max_length=250)
    content     = models.TextField(max_length=2500, blank=True)
    hidden      = models.BooleanField(default=False)
    date        = models.DateTimeField(auto_now_add=True, blank=True)
    entry       = models.ForeignKey(Entry, default=1)
    image       = models.ForeignKey(Image, default=1)
    video       = models.ForeignKey(Video, default=1)

    def __unicode__(self):
        return self.title
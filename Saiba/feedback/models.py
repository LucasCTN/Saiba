from django.contrib.auth.models import Permission, User
from django.db import models
from entry.models import Entry

class Comment(models.Model):
    author = models.ForeignKey(User, default=1)
    entry = models.ForeignKey(Entry, default=1)
    content = models.CharField(max_length=250)
    creation_date = models.DateTimeField(auto_now_add=True, blank=True)
    update_date = models.DateTimeField(auto_now=True, blank=True)
    parent_comment = models.ForeignKey('self', default=None, blank=True, null=True)
    hidden = models.BooleanField(default=False)

    def __unicode__(self):
        text = '#' + str(self.id) + ' - ' + str(self.author.username)
        return text
from django.db.models import Sum
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

    def __unicode__(self):
        text = "#{} - {}".format(self.id, self.author.username)
        if self.parent: 
            text += " (child of #{})".format(self.parent.id)
        return text

    def get_points(self):
        content_type = ContentType.objects.get_for_model(Comment)
        points = Vote.objects.filter(target_id=self.id, target_content_type=content_type).aggregate(Sum('direction'))['direction__sum']
        return points or 0

    def teste(self, arg):
        return arg

    def should_limit_child(self, id, limit):
        if self.id == id:
            return ""
        else:
            return limit
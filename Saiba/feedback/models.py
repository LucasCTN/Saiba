from django.contrib.auth.models import Permission, User
from django.db import models
#from django.contrib.contenttypes.models import ContentType
#from django.contrib.contenttypes.fields import GenericForeignKey

class Vote(models.Model):
    #target_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    #target_id           = models.PositiveIntegerField(null=True, blank=True)
    #target              = GenericForeignKey('target_content_type', 'target_id')
    author              = models.ForeignKey(User, default=1)
    date                = models.DateTimeField(auto_now=True, blank=True)
    type                = models.CharField(max_length=250)
    direction           = models.IntegerField(default=0)

    def __unicode__(self):
        text = '#' + str(self.id) + ' - ' + str(self.author.username)
        return text

class Comment(models.Model):
    #target_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    #target_id           = models.PositiveIntegerField(null=True, blank=True)
    #target              = GenericForeignKey('target_content_type', 'target_id')
    author              = models.ForeignKey(User, default=1)
    content             = models.CharField(max_length=250)
    creation_date       = models.DateTimeField(auto_now_add=True, blank=True)
    update_date         = models.DateTimeField(auto_now=True, blank=True)
    parent_comment      = models.ForeignKey('self', default=None, blank=True, null=True)
    hidden              = models.BooleanField(default=False)

    def __unicode__(self):
        text = '#' + str(self.id) + ' - ' + str(self.author.username)
        return text
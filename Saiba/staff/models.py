from django.db import models

class UserPermission(models.Model):
    code_name = models.CharField(max_length=250, unique=True)
    label = models.CharField(max_length=250)

    def __unicode__(self):
        return self.label + " (" + self.code_name + ")"

class UserGroup(models.Model):
    code_name = models.CharField(max_length=250, unique=True)
    label = models.CharField(max_length=250)
    permissions = models.ManyToManyField(UserPermission)

    def __unicode__(self):
        return self.label + " (" + self.code_name + ")"

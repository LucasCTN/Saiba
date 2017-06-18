from django.db import models

class UserPermission(models.Model):
    code_name = models.CharField(max_length=250, unique=True)
    label = models.CharField(max_length=250)

    def __str__(self):
        return self.label + " (" + self.code_name + ")"

class UserGroup(models.Model):
    code_name = models.CharField(max_length=250, unique=True)
    label = models.CharField(max_length=250)
    permissions = models.ManyToManyField(UserPermission)
    assign_to_staff = models.BooleanField(default=False)

    def __str__(self):
        return self.label + " (" + self.code_name + ")"

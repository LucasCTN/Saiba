from django.contrib.auth.models import Permission, User
from django.template.defaultfilters import slugify
from django.db import models
from staff.models import UserGroup, UserPermission

class Profile(models.Model):
    user        = models.OneToOneField(User, blank=True, null=True, default=None, on_delete=models.CASCADE)
    title       = models.CharField(max_length = 500, blank=True)
    slug        = models.SlugField(max_length=250, default="", blank=True)
    avatar      = models.ImageField(blank=True, upload_to='icon/', default='icon/perfil.png')
    gender      = models.CharField(max_length = 500, blank=True)
    location    = models.CharField(max_length = 500, blank=True)
    about       = models.TextField(max_length = 1500, blank=True)
    groups      = models.ManyToManyField(UserGroup, blank=True)

    def save(self, *args, **kwargs):
        new_user = False
        if not self.id:
            new_user = True
            self.slug = slugify(self.user.username)
        super(Profile, self).save(*args, **kwargs)

        if new_user:
            self.groups.add(UserGroup.objects.get(id=3))

    def __unicode__(self):
        return self.user.username

    def HasPermission(self, permission_code):
        permission = UserPermission.objects.filter(code_name=permission_code).first()

        if permission:
            for group in self.groups.all():
                if group.permissions.filter(id=permission.id).exists():
                    return True
        return False

    def AddGroup(self, group_code):
        group = UserGroup.objects.filter(code_name=group_code).first()

        if group:
            self.groups.add(group)
            self.user.is_staff = group.assign_to_staff
            self.save()

    def RemoveGroup(self, group_code):
        group = UserGroup.objects.filter(code_name=group_code).first()

        if group:
            self.groups.remove(group)

        is_staff = False
        
        for group in self.groups.all():
            if group.assign_to_staff:
                is_staff = True

        self.user.is_staff = is_staff
        self.save()
                
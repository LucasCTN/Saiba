from django.contrib.auth.models import Permission, User
from django.template.defaultfilters import slugify
from django.db import models
from staff.models import UserGroup, UserPermission

class Profile(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE)
    title       = models.CharField(max_length = 500, blank=True)
    slug        = models.SlugField(max_length=250, default="", blank=True)
    avatar      = models.ImageField(blank=True, upload_to='icon/', default='icon/perfil.png')
    gender      = models.CharField(max_length = 500, blank=True)
    location    = models.CharField(max_length = 500)
    about       = models.TextField(max_length = 1500)
    groups      = models.ManyToManyField(UserGroup)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.user.username)

        self.groups.add(UserGroup.objects.get(id=3))
        super(Profile, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.user.username

    def HasPermission(self, permission_label):
        permission = UserPermission.objects.filter(code_name=permission_label).first()

        if permission:
            for group in self.groups.all():
                if group.permissions.filter(id=permission.id).exists():
                    return True
        return False

from django.contrib.auth.models import Permission, User
from django.template.defaultfilters import slugify
from django.db import models

class Profile(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE)
    title       = models.CharField(max_length = 500, blank=True)
    slug        = models.SlugField(max_length=250, default="", blank=True)
    avatar      = models.ImageField(blank=True, upload_to='icon/', default='icon/perfil.png')
    gender      = models.CharField(max_length = 500, blank=True)
    location    = models.CharField(max_length = 500)
    about       = models.CharField(max_length = 1500)    

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.user.username)
        super(Profile, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.user.username
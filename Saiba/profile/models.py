from django.contrib.auth.models import Permission, User
from django.template.defaultfilters import slugify
from django.db import models

class Profile(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE)
    slug        = models.SlugField(max_length=250, default="", blank=True)
    avatar      = models.ImageField(blank=True, upload_to='icon/', default='icon/perfil.png')
    gender      = models.CharField(max_length = 100, choices = (('Ele', 'Ele'), ('Ela', 'Ela'), ('Ele(a)', 'Ele(a)')))
    location    = models.CharField(max_length = 500, blank=True)
    about       = models.CharField(max_length = 1500, blank=True)    

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.user.username)
        super(Profile, self).save(*args, **kwargs)
        
        
        
from datetime import datetime, timedelta

from django.contrib.auth.models import Permission, User
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.crypto import get_random_string

from staff.models import UserGroup, UserPermission

from .managers import ProfileManager, TokenManager

def generate_code():
    '''Returns a random 32 character string for Tokens.'''
    return get_random_string(length=32)

def generate_expiration_date():
    '''Returns the date of 7 days from now.'''
    return datetime.now() + timedelta(days=7)

class Profile(models.Model):
    user        = models.OneToOneField(User, blank=True, null=True, default=None, on_delete=models.CASCADE)
    title       = models.CharField(max_length = 500, blank=True)
    slug        = models.SlugField(max_length=250, default="", blank=True)
    avatar      = models.ImageField(blank=True, upload_to='avatars/', default='home/images/assets/avatar_default.svg')
    gender      = models.CharField(max_length = 500, blank=True)
    location    = models.CharField(max_length = 500, blank=True)
    about       = models.TextField(max_length = 1500, blank=True)
    groups      = models.ManyToManyField(UserGroup, blank=True)
    is_email_activated = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)

    objects = ProfileManager()

    def save(self, *args, **kwargs):
        new_user = False
        if not self.id:
            new_user = True
            self.slug = slugify(self.user.username)
        super(Profile, self).save(*args, **kwargs)

        if new_user:
            self.groups.add(UserGroup.objects.get(id=3))

    def __str__(self):
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

class Token(models.Model):
    '''Multi-purpose model for confirmations Tokens. Used for activating e-mail.'''
    related_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    code = models.CharField(max_length=32, default=generate_code, unique=True)
    expiration_date = models.DateTimeField(default=generate_expiration_date)

    objects = TokenManager()

    def __str__(self):
        return self.code

    def change_expiration_date(self, days):
        '''Defines how many days since now the token should expire.'''
        self.expiration_date = datetime.now() + timedelta(days=days)
        self.save()

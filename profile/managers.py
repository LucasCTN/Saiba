# -*- coding: utf-8 -*-
from datetime import date

from django.db import models

today = date.today()

class TokenQueryset(models.query.QuerySet):
    def active(self):
        return self.filter(expiration_date__gte=today)

class ProfileQueryset(models.query.QuerySet):
    def active(self):
        return self.filter(is_email_activated=True, is_banned=False)

class ProfileManager(models.Manager):
    '''Custom manager for Profiles.'''
    def get_queryset(self):
        return TokenQueryset(self.model, using=self._db)

    def active(self):
        '''Returns a QuerySet with only for valid Profiles.'''
        return self.get_queryset().active()

class TokenManager(models.Manager):
    '''Custom manager for Profiles.'''
    def get_queryset(self):
        return TokenQueryset(self.model, using=self._db)

    def active(self):
        '''Returns a QuerySet with only Tokens that aren't expired.'''
        return self.get_queryset().active()

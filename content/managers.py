# -*- coding: utf-8 -*-
from django.db import models

class BPostManager(models.Manager):
    '''Custom manager for BPosts.'''
    def active(self):
        '''Returns a QuerySet with only BPosts that aren't hidden.'''
        return self.get_queryset().filter(hidden=False)

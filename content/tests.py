# -*- coding: utf-8 -*-
import django
from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory
from entry.models import Entry, Category, Revision
from profile.models import Profile
from entry.views import create_entry

# TODO: Configure your database in settings.py and sync before running tests.
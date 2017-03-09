# -*- coding: utf-8 -*-
import django
from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory
from entry.models import Entry
from entry.views import create_entry

# TODO: Configure your database in settings.py and sync before running tests.


class EntryTestCase(TestCase):
    """Tests for the entry views."""

    @classmethod
    def setUpClass(cls):
        cls.factory = RequestFactory()
        cls.user = User.objects.create_user(
            username='Joao', email='joao@…', password='top_secret')
        django.setup()

    def test_create_entry(self):
        """
        Tests creating a entry.
        """
        request = self.factory.get('/entrada/nova-entrada/')
        request.user = self.user

        response = create_entry(request)
        self.assertEqual(response.status_code, 200)
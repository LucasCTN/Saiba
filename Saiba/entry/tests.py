# -*- coding: utf-8 -*-
import django
from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory
from entry.models import Entry, Category, Revision
from profile.models import Profile
from entry.views import create_entry

# TODO: Configure your database in settings.py and sync before running tests.


class EntryTestCase(TestCase):
    """Tests for the entry views."""

    @classmethod
    def setUpTestData(self):
        django.setup()
        self.factory = RequestFactory()
        self.category = Category.objects.create(label='Meme', description='Meem')
        self.user = User.objects.create_user(username='Joao', email='joao@…', password='top_secret')
        profile = Profile.objects.create(user=self.user)
        profile.save()

    def test_create_entry(self):
        """
        Tests creating a entry.
        """

        tag_list = ['consectetur', 'adipiscing', 'elit']
        request = self.factory.post('/entrada/nova-entrada', 
                                    {'title': 'Lorem', 'origin': 'Ipsum', 'date_origin': '12 de fevereiro de 2016', 'category': 1, 
                                     'content': 'Sit amet', 'tags-selected': ",".join(tag_list)}, 
                                    follow=True)
        request.user = self.user
        response = create_entry(request)

        entry = Entry.objects.get(pk=1)
        revision = Revision.objects.filter(entry=entry).first()

        self.assertEqual(entry.pk, 1)
        self.assertEqual(entry.title, "Lorem")
        self.assertEqual(entry.origin, "Ipsum")
        self.assertEqual(entry.date_origin, "12 de fevereiro de 2016")
        self.assertEqual(entry.category.pk, 1)
        self.assertEqual(revision.content, "Sit amet")

        for tag in entry.tags.all():
            self.assertTrue((tag.label in tag_list))
        #self.assertEqual(response.status_code, 200)
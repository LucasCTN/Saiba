# -*- coding: utf-8 -*-
from django import forms
from .models import Entry, Revision

from Saiba import custom_messages

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = [ "title", "category", "origin", "date_origin", "icon", "tags" ]

        labels = {
            'title': ('Título'),
            'category': ('Categoria'),
            'origin': ('Origem'),
            'date_origin': ('Data'),
            'icon': ('Ícone'),
            'tags': ('Marcações'),
        }

        error_messages = custom_messages.custom_error_messages(fields, labels)

class RevisionForm(forms.ModelForm):
    class Meta:
        model = Revision
        fields = [ "content" ]

        widgets = {
          'content': forms.Textarea(attrs={'rows':50}),
        }

        labels = {
            'content': ('Conteúdo'),
        }

        error_messages = custom_messages.custom_error_messages(fields, labels)
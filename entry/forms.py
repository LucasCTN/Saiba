# -*- coding: utf-8 -*-
from django import forms
from .models import Entry, Revision, Category

from saiba import custom_messages

class EntryForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(EntryForm, self).clean()
        icon = cleaned_data.get("icon")
        icon_url = cleaned_data.get("icon_url")

        if bool(icon) == bool(icon_url):
            raise forms.ValidationError(
                "A entrada precisa de um ícone (não envie duas imagens)."
            )

    class Meta:
        model = Entry
        fields = [ "title", "category", "origin", "date_origin", "icon", "icon_url", "tags" ]

        labels = {
            'title': ('Título'),
            'category': ('Categoria'),
            'origin': ('Origem'),
            'date_origin': ('Data'),
            'icon': ('Ícone'),
            'icon_url': ('Link do ícone'),
            'tags': ('Marcações'),
        }

        widgets = {
          'title': forms.TextInput(attrs={'class': 'form-control form-title'}),
          'category': forms.Select(attrs={'class': 'form-control form-category'}),
          'origin': forms.TextInput(attrs={'class': 'form-control form-origin'}),
          'date_origin': forms.Textarea(attrs={'class': 'form-control form-date_origin'}),
          'icon': forms.FileInput(attrs={'class': 'form-control-file form-icon', 'id': 'id_entry_icon'}),
          'icon_url': forms.TextInput(attrs={'class': 'form-control form-state', 'placeholder': 'Coloque aqui um link para uma imagem.'}),
        }

        error_messages = custom_messages.get_all_error_messages(fields, labels)

class StaffEntryForm(forms.ModelForm):
    icon_url = forms.URLField(widget=forms.TextInput(attrs={'placeholder': 'Coloque aqui um link para uma imagem.',
        'class': 'form-control form-state'}), required=False)
    icon = forms.ImageField(widget=forms.FileInput(attrs={'id': 'id_entry_icon'}), required=False)

    def clean(self):
        cleaned_data = super(StaffEntryForm, self).clean()
        icon = cleaned_data.get("icon")
        icon_url = cleaned_data.get("icon_url")

        if bool(icon) == bool(icon_url):
            raise forms.ValidationError(
                "A entrada precisa de um ícone (não envie duas imagem)."
            )

    class Meta:
        model = Entry
        fields = ["title", "category", "origin", "date_origin", "icon", "icon_url", "tags",
                  "images_locked", "videos_locked", "comments_locked", "hidden"]

        labels = {
            'title': ('Título'),
            'category': ('Categoria'),
            'origin': ('Origem'),
            'date_origin': ('Data'),
            'icon': ('Ícone'),
            'icon_url': ('Link do ícone'),
            'tags': ('Marcações'),
            'images_locked': ('Imagens trancadas'),
            'videos_locked': ('Vídeos trancados'),
            'comments_locked': ('Comentários trancados'),
            'hidden': ('Entrada escondida'),
        }

        error_messages = custom_messages.get_all_error_messages(fields, labels)

class RevisionForm(forms.ModelForm):
    class Meta:
        model = Revision
        fields = [ "content" ]

        widgets = {
          'content': forms.Textarea(attrs={'class': 'form-control form-content', 'rows': 50}),
        }

        labels = {
            'content': ('Conteúdo'),
        }

        error_messages = custom_messages.get_all_error_messages(fields, labels)
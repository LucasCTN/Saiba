# -*- coding: utf-8 -*-
from django import forms
from .models import BPost

class BPostForm(forms.ModelForm):
    icon_url = forms.URLField(widget=forms.TextInput(
        attrs={'placeholder': 'Coloque aqui um link para uma imagem.',
               'class': 'form-control form-state'}), required=False)
    icon = forms.ImageField(widget=forms.FileInput(attrs={'id': 'id_entry_icon'}), required=False)

    def clean(self):
        cleaned_data = super(BPostForm, self).clean()
        icon = cleaned_data.get("icon")
        icon_url = cleaned_data.get("icon_url")

        if bool(icon) and bool(icon_url):
            raise forms.ValidationError("Não envie duas imagens para a postagem.")

    class Meta:
        model = BPost
        fields = ["title", "category", "content", "icon", "icon_url", "tags", "comments_locked", "hidden"]

        labels = {
            'title': ('Título'),
            'category': ('Categoria'),
            'origin': ('Origem'),
            'date_origin': ('Data'),
            'icon': ('Ícone'),
            'icon_url': ('Link do ícone'),
            'tags': ('Marcações'),
        }

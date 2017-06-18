# -*- coding: utf-8 -*-
from django.forms import ModelForm
from .models import Image, Video
from django import forms

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.files.base import ContentFile

from PIL import Image as ImagePIL
import urllib

class ImageForm(ModelForm):
    file_url = forms.URLField(widget=forms.TextInput(attrs={'placeholder': 'Coloque aqui um link para uma imagem.',
        'class': 'form-control form-state'}), required=False)

    def clean(self):
        cleaned_data = super(ImageForm, self).clean()
        file = cleaned_data.get("file")
        file_url = cleaned_data.get("file_url")

        if bool(file) == bool(file_url):
            raise forms.ValidationError(
                "Preencha somente um destes campos"
            )

        if file_url and not self.image_validity(file_url):
            raise forms.ValidationError(
                "A imagem inserida é inválida."
            )

    def image_validity(self, file_url):
        img_temp = NamedTemporaryFile()
        img_temp.write(urllib.request.urlopen(file_url).read())
        img_temp.flush()

        image_file = File(img_temp)

        try:
            ImagePIL.open(image_file)
            return True
        except:
            return False

    class Meta:
        model = Image
        fields = [ "title", "source", "date_origin", "description", "file", "file_url", "state" ]

        widgets = {
          'title': forms.TextInput(attrs={'class': 'form-control form-title'}),
          'file': forms.FileInput(attrs={'class': 'form-control-file form-file'}),
          'source': forms.TextInput(attrs={'class': 'form-control form-source'}),
          'date_origin': forms.TextInput(attrs={'class': 'form-control form-date_origin'}),
          'description': forms.Textarea(attrs={'class': 'form-control form-description'}),
          'state': forms.Select(attrs={'class': 'form-control form-state'}),
        }

class StaffImageForm(ModelForm):
    file_url = forms.URLField(widget=forms.TextInput(attrs={'placeholder': 'Coloque aqui um link para uma imagem.',
        'class': 'form-control form-state'}), required=False)

    def clean(self):
        cleaned_data = super(StaffImageForm, self).clean()
        file = cleaned_data.get("file")
        file_url = cleaned_data.get("file_url")

        if bool(file) == bool(file_url):
            raise forms.ValidationError(
                "Preencha somente um destes campos"
            )

        if file_url and not self.image_validity(file_url):
            raise forms.ValidationError(
                "A imagem inserida é inválida."
            )

    def image_validity(self, file_url):
        img_temp = NamedTemporaryFile()
        img_temp.write(urllib.request.urlopen(file_url).read())
        img_temp.flush()

        image_file = File(img_temp)

        try:
            ImagePIL.open(image_file)
            return True
        except:
            return False

    class Meta:
        model = Image
        fields = [ "title", "source", "date_origin", "description", "file", "file_url", "state", "comments_locked", "hidden" ]

        widgets = {
          'title': forms.TextInput(attrs={'class': 'form-control form-title'}),
          'source': forms.TextInput(attrs={'class': 'form-control form-source'}),
          'date_origin': forms.TextInput(attrs={'class': 'form-control form-date_origin'}),
          'description': forms.Textarea(attrs={'class': 'form-control form-description'}),
        }

class VideoForm(ModelForm):
    class Meta:
        model = Video
        fields = [ "title", "date_origin", "description", "media", "state" ]

        widgets = {
          'title': forms.TextInput(attrs={'class': 'form-control form-title'}),
          'media': forms.TextInput(attrs={'class': 'form-control-file form-media'}),
          'date_origin': forms.TextInput(attrs={'class': 'form-control form-date_origin'}),
          'description': forms.Textarea(attrs={'class': 'form-control form-description'}),
          'state': forms.Select(attrs={'class': 'form-control form-state'}),
        }

class StaffVideoForm(ModelForm):
    class Meta:
        model = Video
        fields = [ "title", "date_origin", "description", "media", "state", "comments_locked", "hidden" ]

        widgets = {
          'title': forms.TextInput(attrs={'class': 'form-control form-title'}),
          'date_origin': forms.TextInput(attrs={'class': 'form-control form-date_origin'}),
          'description': forms.Textarea(attrs={'class': 'form-control form-description'}),
        }
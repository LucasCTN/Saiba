# -*- coding: utf-8 -*-
from django.forms import ModelForm
from .models import Image, Video
from django import forms

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.files.base import ContentFile
import urllib2

from PIL import Image as ImagePIL

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
            print "estou aqui"
            raise forms.ValidationError(
                "A imagem inserida é inválida."
            )

    def image_validity(self, file_url):
        img_temp = NamedTemporaryFile()
        img_temp.write(urllib2.urlopen(file_url).read())
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
            print "estou aqui"
            raise forms.ValidationError(
                "A imagem inserida é inválida."
            )

    def image_validity(self, file_url):
        img_temp = NamedTemporaryFile()
        img_temp.write(urllib2.urlopen(file_url).read())
        img_temp.flush()

        image_file = File(img_temp)

        try:
            ImagePIL.open(image_file)
            return True
        except:
            return False

    class Meta:
        model = Image
        fields = [ "title", "source", "date_origin", "description", "file", "file_url", "state", "comments_locked" ]

class VideoForm(ModelForm):
    class Meta:
        model = Video
        fields = [ "title", "date_origin", "description", "link", "state", "link" ]

class StaffVideoForm(ModelForm):
    class Meta:
        model = Video
        fields = [ "title", "date_origin", "description", "link", "state", "link", "comments_locked" ]
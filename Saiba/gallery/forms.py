from django.forms import ModelForm
from .models import Image, Video
from django import forms

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

    class Meta:
        model = Image
        fields = [ "title", "source", "date_origin", "description", "file", "file_url", "state" ]

class VideoForm(ModelForm):
    class Meta:
        model = Video
        fields = [ "title", "date_origin", "description", "link", "state", "link" ]
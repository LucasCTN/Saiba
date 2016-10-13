from django.forms import ModelForm
from .models import Image, Video

class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = [ "author", "title", "source", "tags", "description", "file", "state" ]

class VideoForm(ModelForm):
    class Meta:
        model = Video
        fields = [ "author", "title", "tags", "description", "link", "state" ]
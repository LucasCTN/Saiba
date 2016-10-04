from django.forms import ModelForm
from .models import Image, Video

class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = [ "author", "title", "source", "tags", "entry", "description", "file", "state" ]

class VideoForm(ModelForm):
    class Meta:
        model = Video
        fields = [ "author", "title", "tags", "entry", "description", "link", "state" ]
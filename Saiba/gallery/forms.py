from django.forms import ModelForm
from .models import Image, Video

class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = [ "title", "source", "date_origin", "description", "file", "state" ]

class VideoForm(ModelForm):
    class Meta:
        model = Video
        fields = [ "title", "date_origin", "description", "link", "state" ]
from django.forms import ModelForm
from .models import Entry, Revision
from feedback.models import EntryComment, ImageComment

class EntryForm(ModelForm):
    class Meta:
        model = Entry
        fields = [ "title", "category", "origin", "additional_references", "icon" ]

class RevisionForm(ModelForm):
    class Meta:
        model = Revision
        fields = [ "content" ]

class EntryCommentForm(ModelForm):
    class Meta:
        model = EntryComment
        fields = [ "content" ]

class ImageCommentForm(ModelForm):
    class Meta:
        model = ImageComment
        fields = [ "content" ]        
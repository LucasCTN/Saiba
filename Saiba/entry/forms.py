from django.forms import ModelForm
from .models import Entry, Revision
from feedback.models import Comment

class EntryForm(ModelForm):
    class Meta:
        model = Entry
        fields = [ "title", "category", "origin", "additional_references", "icon" ]

class RevisionForm(ModelForm):
    class Meta:
        model = Revision
        fields = [ "content" ]

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = [ "content" ]
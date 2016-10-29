from django.forms import ModelForm
from .models import Entry, Revision, EditorList

class EntryForm(ModelForm):
    class Meta:
        model = Entry
        fields = [ "title", "category", "origin", "additional_references", "icon" ]

class RevisionForm(ModelForm):
    class Meta:
        model = Revision
        fields = [ "content" ]

class EditorListForm(ModelForm):
    class Meta:
        model = EditorList
        fields = [ "user" ]  
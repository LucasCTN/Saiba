from django import forms
from .models import Entry, Revision

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = [ "title", "category", "origin", "additional_references", "icon" ]


class RevisionForm(forms.ModelForm):
    class Meta:
        model = Revision
        fields = [ "content" ]
        widgets = {
          'content': forms.Textarea(attrs={'rows':50}),
        }
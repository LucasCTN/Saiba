from rest_framework import serializers
from .models import Entry, Revision

class EntrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Entry
        #field = '__all__'
        field = ('author', 'title', 'slug', 'status', 'category', 'type', 'origin', 'additional_references', 'icon')

class RevisionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Revision
        #field = '__all__'
        field = ('author', 'entry', 'content', 'date')
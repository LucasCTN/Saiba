from rest_framework import serializers
from .models import Image

class ImageSerializer(serializers.ModelSerializer):
    def to_representation(self, obj):
        representation = super(ImageSerializer, self).to_representation(obj)
        representation.pop('trending_points')
        representation.pop('hidden')
        return representation

    class Meta:
        model = Image
        #field = '__all__'
        field = ('author', 'title', 'date', 'source', 'tags', 'entry', 'file', 'description')
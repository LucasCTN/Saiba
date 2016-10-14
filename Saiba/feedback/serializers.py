from rest_framework import serializers
from .models import Comment, Vote

class CommentSerializer(serializers.ModelSerializer):
    def to_representation(self, obj):
        representation = super(CommentSerializer, self).to_representation(obj)
        representation.pop('hidden')
        representation.pop('target_content_type')
        representation.pop('target_id')
        return representation

    class Meta:
        model = Comment
        #field = '__all__'
        field = ('author', 'content', 'creation_date', 'update_date', 'parent_comment')

class VoteSerializer(serializers.ModelSerializer):
    def to_representation(self, obj):
        representation = super(VoteSerializer, self).to_representation(obj)
        representation.pop('target_content_type')
        representation.pop('target_id')
        return representation

    class Meta:
        model = Vote
        field = ('author', 'date', 'direction', 'creation_date', 'update_date')
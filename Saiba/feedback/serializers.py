from django.db.models import Sum
from rest_framework import pagination, serializers
from django.contrib.contenttypes.models import ContentType
from .models import Comment, Vote

class VoteSerializer(serializers.ModelSerializer):
    def to_representation(self, obj):
        representation = super(VoteSerializer, self).to_representation(obj)
        representation.pop('target_content_type')
        representation.pop('target_id')
        return representation

    class Meta:
        model = Vote
        field = ('author', 'date', 'direction', 'creation_date', 'update_date')

class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    points  = serializers.IntegerField(required=False, read_only=True)
    author_username = serializers.StringRelatedField(source='author.username', read_only=True)
    author_slug = serializers.StringRelatedField(source='author.profile.slug', read_only=True)
    author_avatar = serializers.StringRelatedField(source='author.profile.avatar', read_only=True)

    def get_replies(self, obj):
        return None

    def to_representation(self, obj):
        representation = super(CommentSerializer, self).to_representation(obj)
        representation.pop('hidden')
        representation.pop('target_content_type')
        representation.pop('target_id')
        return representation    

    class Meta:
        model = Comment
        #field = '__all__'
        field = ('author', 'content', 'creation_date', 'update_date', 'parent_comment', 'replies', 'points', 'parent', 'reply_to')

class PointsSerializer(serializers.Serializer):
    points              = serializers.IntegerField()
    target_id           = serializers.IntegerField(required=False)
    target_content_type = serializers.IntegerField(required=False)

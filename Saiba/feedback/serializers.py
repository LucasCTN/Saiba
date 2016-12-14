from rest_framework import pagination, serializers
from django.contrib.contenttypes.models import ContentType
from .models import Comment, Vote, Reply

class VoteSerializer(serializers.ModelSerializer):
    def to_representation(self, obj):
        representation = super(VoteSerializer, self).to_representation(obj)
        representation.pop('target_content_type')
        representation.pop('target_id')
        return representation

    class Meta:
        model = Vote
        field = ('author', 'date', 'direction', 'creation_date', 'update_date')

class ReplySerializer(serializers.ModelSerializer):
    points = serializers.IntegerField(required=False, read_only=True)

    def to_representation(self, obj):
        representation = super(ReplySerializer, self).to_representation(obj)
        representation.pop('hidden')
        return representation    

    class Meta:
        model = Reply
        field = ('author', 'content', 'creation_date', 'update_date', 'comment', 'response_to', 'points')

class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    points  = serializers.IntegerField(required=False, read_only=True)
    author_username = serializers.StringRelatedField(source='author.username', read_only=True)
    author_slug = serializers.StringRelatedField(source='author.profile.slug', read_only=True)
    author_avatar = serializers.StringRelatedField(source='author.profile.avatar', read_only=True)

    def get_replies(self, obj):
        if 'reply_limit' in self.context:
            limit = int(self.context['reply_limit'])

            query = Reply.objects.filter(comment=obj).order_by('id')

            if limit != 0:
                query = query[:limit]

            serializer = ReplySerializer(query, many=True)
            return serializer.data
        else:
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
        field = ('author', 'content', 'creation_date', 'update_date', 'parent_comment', 'replies', 'points')

class PointsSerializer(serializers.Serializer):
    points              = serializers.IntegerField()
    target_id           = serializers.IntegerField(required=False)
    target_content_type = serializers.IntegerField(required=False)

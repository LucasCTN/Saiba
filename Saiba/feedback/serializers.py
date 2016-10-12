from rest_framework import serializers
from .models import Comment, CommentVote

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        #field = '__all__'
        field = ('author', 'content', 'creation_date', 'update_date', 'parent_comment')

class CommentVoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommentVote
        #field = '__all__'
        field = ('comment', 'comment')
from rest_framework import serializers
from .models import Comment, Vote

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        field = ('content', 'creation_date', 'update_date', 'parent_comment')

    def to_representation(self, obj):
        ret = super(CommentSerializer, self).to_representation(obj)
        ret.pop('votes')
        ret.pop('hidden')
        return ret 

class VoteSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Vote
        #field = '__all__'
        field = ('target', 'direction')

class CommentVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        field = ('target', 'direction')
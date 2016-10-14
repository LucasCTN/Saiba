from django.shortcuts import render, get_object_or_404
from django.views import generic
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from entry.models import Entry, Revision
from entry.serializers import EntrySerializer, RevisionSerializer
from feedback.models import Comment, Vote
from feedback.serializers import CommentSerializer
from django.contrib.contenttypes.models import ContentType

class EntryDetail(APIView):

    def get(self, request, slug):
        #entries = Entry.objects.all()
        entry = get_object_or_404(Entry, slug=slug)
        serializer = EntrySerializer(entry, many=False)
        return Response(serializer.data)

    def post(self, request, slug):
        serializer = EntrySerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HistoricDetail(APIView):

    def get(self, request, slug):
        #articles = Entry.objects.all()
        entry = get_object_or_404(Entry, slug=slug)
        revisions = Revision.objects.filter(entry=entry, hidden=False)
        serializer = RevisionSerializer(revisions, many=True)
        return Response(serializer.data)

class CommentDetail(APIView):
    def get(self, request):
        comment_target_id   = request.GET.get('id')
        comment_target_slug = request.GET.get('slug')
        comment_target_type = request.GET.get('type')

        if comment_target_type is not None and comment_target_type == "entry" and comment_target_slug is not None:
            entry_type_id    = ContentType.objects.get_for_model(Entry).id
            entry       = get_object_or_404(Entry, slug=comment_target_slug)
            comments = Comment.objects.filter(target_id=entry.id, target_content_type=entry_type_id)
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    '''def post(self, request, slug):
        serializer = EntrySerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)'''

class CommentVote(APIView):
    pass
    '''def post(self, request):
        if request.GET.get('id'):
            comment_id      = int(request.GET.get('id'))
            direction       = int(request.GET.get('direction'))
            comment         = EntryComment.objects.get(pk=comment_id)

            vote            = CommentVote()
            vote.comment    = comment
            vote.author     = request.user
            vote.direction  = direction
            vote.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)'''
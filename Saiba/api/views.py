#from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, get_object_or_404
from django.views import generic
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from entry.models import Entry, Revision
from entry.serializers import EntrySerializer, RevisionSerializer
from gallery.models import Image, Video
from feedback.serializers import CommentSerializer, VoteSerializer
from feedback.models import Vote, Comment

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
        content_id      = self.request.query_params.get('id', None)
        entry_slug      = self.request.query_params.get('slug', None)
        content_type    = self.request.query_params.get('type', None)
        
        if entry_slug is not None:
            entry = Entry.objects.get(slug=entry_slug)
            comments = entry.comments.filter(hidden=False)
        elif content_id is not None and content_type is not None:
            if content_type == "image":
                image = Image.objects.get(pk=content_id)
                comments = image.comments.filter(hidden=False)
            elif content_type == "video":
                video = Video.objects.get(pk=content_id)
                comments = video.comments.filter(hidden=False)

        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    '''def get(self, request, slug):
        #entries = Entry.objects.all()
        comments_each_page = 5

        index = int(request.GET.get('index'))        

        if index:
            entry = get_object_or_404(Entry, slug=slug)
            comments = list(Comment.objects.all().filter(entry=entry, hidden=False).order_by('-creation_date'))[index-1:index+1]
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, slug):
        serializer = EntrySerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)'''


class CommentVote(APIView):
    def get(self, request):
        comment_id = self.request.query_params.get('id', None)
        
        if comment_id is not None:
            comment = Comment.objects.get(id=comment_id)

        serializer = CommentSerializer(comment, many=False)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        data["target_id"]           = data["id"]
        #data["target_content_type"] = ContentType.objects.get_for_model(Comment).id
        serializer = VoteSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
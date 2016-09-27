from django.shortcuts import render, get_object_or_404
from django.views import generic
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from entry.models import Entry, Revision
from entry.serializers import EntrySerializer, RevisionSerializer
from feedback.models import Comment
from feedback.serializers import CommentSerializer

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

    def get(self, request, slug):
        #entries = Entry.objects.all()
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
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
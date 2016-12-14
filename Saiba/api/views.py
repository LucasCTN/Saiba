from django.db.models import Sum
from django.shortcuts import render, get_object_or_404
from django.views import generic
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from entry.models import Entry, Revision
from entry.serializers import EntrySerializer, RevisionSerializer
from feedback.models import Comment, Vote, Reply
from feedback.serializers import CommentSerializer, VoteSerializer, ReplySerializer, PointsSerializer
from gallery.models import Image, Video
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from rest_framework.pagination import PageNumberPagination
import Saiba.utils

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
        comment_id      = request.GET.get('id')
        reply_limit     = request.GET.get('reply_limit')

        if reply_limit is None:
            reply_limit = 0

        if comment_id is not None:
            comment = get_object_or_404(Comment, pk=comment_id)
            serializer = CommentSerializer(comment, many=False, context={"reply_limit":reply_limit})
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        data = request.data.copy()
        data['points'] = 0

        if data['type']:
            comment_target_type = data['type']

            if comment_target_type == "entry" and data['slug'] is not None:
                data["target_content_type"] = ContentType.objects.get_for_model(Entry).id
                data["target_id"]           = get_object_or_404(Entry, slug=data["slug"]).pk
            elif comment_target_type == "image" and data['id'] is not None:
                data["target_content_type"] = ContentType.objects.get_for_model(Image).id
                data["target_id"]           = data['id']
            elif comment_target_type == "video" and data['id'] is not None:                
                data["target_content_type"] = ContentType.objects.get_for_model(Video).id
                data["target_id"]           = data['id']

        serializer = CommentSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request):
        """Parameters: id and content"""
        data = request.data.copy()

        if data['id'] is not None:
            vote = get_object_or_404(Vote, pk=data['id'])

        serializer = VoteSerializer(vote, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReplyDetail(APIView):
    def get(self, request):
        reply_id      = request.GET.get('id')

        if reply_id:
            reply = get_object_or_404(Reply, pk=reply_id)
            serializer = ReplySerializer(reply, many=False)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        data = request.data.copy()
        data['points'] = 0

        serializer = ReplySerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request):
        """Parameters: id and content"""
        data = request.data.copy()

        if data['id'] is not None:
            reply = get_object_or_404(Reply, pk=data['id'])

        serializer = ReplySerializer(vote, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VoteDetail(APIView):
    def get(self, request):
        vote_target_id   = request.GET.get('id')
        vote_target_type = request.GET.get('type')

        if vote_target_type is not None:
            if vote_target_type == "comment" and vote_target_id:
                comment_type_id = ContentType.objects.get_for_model(Comment).id
                comment         = get_object_or_404(Comment, pk=vote_target_id)
                votes           = Vote.objects.filter(target_id=comment.id, target_content_type=comment_type_id)
                serializer      = VoteSerializer(votes, many=True)
                return Response(serializer.data)
            elif vote_target_type == "image" and vote_target_id:
                image_type_id   = ContentType.objects.get_for_model(Image).id
                image           = get_object_or_404(Image, pk=vote_target_id)
                votes           = Vote.objects.filter(target_id=image.id, target_content_type=image_type_id)
                serializer      = VoteSerializer(votes, many=True)
                return Response(serializer.data)
            elif vote_target_type == "video" and vote_target_id:                
                video_type_id   = ContentType.objects.get_for_model(Video).id
                video           = get_object_or_404(Image, pk=vote_target_id)
                votes           = Vote.objects.filter(target_id=video.id, target_content_type=video_type_id)
                serializer      = VoteSerializer(votes, many=True)
                return Response(serializer.data)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        data = request.data.copy()

        id = request.POST.get('id', False)
        type = request.POST.get('type', False)
        direction = request.POST.get('direction', False)

        if type and id and Saiba.utils.is_valid_direction(direction):
            vote_target_type = type
            data["target_id"] = id

            if vote_target_type == "comment":
                data["target_content_type"] = ContentType.objects.get_for_model(Comment).id
            elif vote_target_type == "image":
                data["target_content_type"] = ContentType.objects.get_for_model(Image).id
            elif vote_target_type == "video":                
                data["target_content_type"] = ContentType.objects.get_for_model(Video).id

        serializer = VoteSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request):
        """Parameters: id and direction"""
        data = request.data.copy()

        if data['id'] is not None:
            vote = get_object_or_404(Vote, pk=data['id'])

        serializer = VoteSerializer(vote, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentPageDetail(APIView):
    def get(self, request):
        comment_target_id   = request.GET.get('id')
        comment_target_slug = request.GET.get('slug')
        comment_target_type = request.GET.get('type')
        reply_limit         = request.GET.get('reply_limit')
        comments = []

        target_type_id = 0
        target_id      = 0

        if comment_target_type is not None:
            if comment_target_type == "entry" and comment_target_slug:
                entry           = get_object_or_404(Entry, slug=comment_target_slug)
                target_type_id  = ContentType.objects.get_for_model(Entry).id
                target_id = entry.id
            elif comment_target_type == "image" and comment_target_id:
                image           = get_object_or_404(Image, id=comment_target_id)
                target_type_id  = ContentType.objects.get_for_model(Image).id
                target_id = image.id
            elif comment_target_type == "video" and comment_target_id:                
                video           = get_object_or_404(Image, id=comment_target_id)
                target_type_id  = ContentType.objects.get_for_model(Video).id
                target_id = video.id

            comments = Comment.objects.filter(target_id=target_id, 
                                              target_content_type=target_type_id).order_by('-creation_date')

        for comment in comments:
            comment_type_id = ContentType.objects.get_for_model(Comment).id
            comment.points = (Vote.objects.filter(target_id=comment.pk, 
                                              target_content_type=comment_type_id).aggregate(Sum('direction')))['direction__sum']
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(comments, request)

        serializer = CommentSerializer(result_page, many=True, context={"reply_limit":reply_limit})
        return paginator.get_paginated_response(serializer.data)        
        #return Response(status=status.HTTP_400_BAD_REQUEST)

class PointsDetail(APIView):
    def get(self, request):
        vote_target_id   = request.GET.get('id')
        vote_target_slug = request.GET.get('slug')
        vote_target_type = request.GET.get('type')

        target_type_id = None
        target_id      = None

        type_content_map = {'comment': Comment, 'reply': Reply }

        if vote_target_type is not None:
            target_type = type_content_map[vote_target_type]

            target         = get_object_or_404(target_type, id=vote_target_id)
            target_type_id = ContentType.objects.get_for_model(target_type).id
            target_id       = target.id

        points = {}
        points['points'] = (Vote.objects.filter(target_id=target_id, target_content_type=target_type_id)
                            .aggregate(Sum('direction')))['direction__sum']

        serializer = PointsSerializer(points)        
        return Response(serializer.data)
        
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
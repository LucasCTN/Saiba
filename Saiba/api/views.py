from profile.models import Profile

from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.db import connection
from django.db.models import Count, F, Sum
from django.shortcuts import get_object_or_404, render
from django.views import generic
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

import Saiba.parser
import Saiba.utils
from entry.models import Entry, Revision
from entry.serializers import EntrySerializer, RevisionSerializer
from feedback.models import Comment, TrendingVote, Vote
from feedback.serializers import (CommentSerializer, PointsSerializer,
                                  VoteSerializer)
from gallery.models import Image, Video
from gallery.serializers import ImageSerializer
from home.models import SaibaSettings


class EntryDetail(APIView):
    def get(self, request):
        slug = request.GET.get('slug')

        entry = Entry.objects.filter(Entry, slug=slug).first()
        serializer = EntrySerializer(entry, many=False)

        if slug:
            if entry:
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        data = request.data.copy()
        data['author'] = request.user.id

        serializer = EntrySerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        data['author'] = request.user.id

        types_map = { "comment": Comment, "image": Image, "video": Video, "entry": Entry, "profile": Profile }
        target_type = types_map[data["type"]]

        data["target_content_type"] = ContentType.objects.get_for_model(target_type).id
        data["target_id"]           = data['id']

        serializer = CommentSerializer(data=data)
        target_id = data['id']

        if serializer.is_valid():
            target = None
            vote_type_model = SaibaSettings.objects.get(type='trending_weight_comment')

            if target_type == Entry:
                target = Entry.objects.get(id=target_id)

                if target.comments_locked:
                    return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

                trending_vote = TrendingVote.objects.create(author=request.user, entry=target,
                                                            vote_type=vote_type_model)

            elif target_type == Image:
                target = Image.objects.get(id=target_id)

                if target.comments_locked:
                    return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

                trending_vote = TrendingVote.objects.create(author=request.user, image=target,
                                                            vote_type=vote_type_model)
            elif target_type == Video:
                target = Video.objects.get(id=target_id)

                if target.comments_locked:
                    return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

                trending_vote = TrendingVote.objects.create(author=request.user, video=target,
                                                            vote_type=vote_type_model)

            new_comment = serializer.save()

            if new_comment.reply_to:
                new_comment.create_action("2")
            else:
                new_comment.create_action("1")

            new_vote = Vote.objects.create(target=new_comment, author=request.user,
                                           direction=1) # Vote in own comment
            new_vote.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        """Parameters: id and is_deleted"""
        data = request.data.copy()
        is_deleted = data["is_deleted"]
        args = {"is_deleted": is_deleted}

        if data['id']:
            comment = get_object_or_404(Comment, pk=data['id'])

        serializer = CommentSerializer(comment, data=args, partial=True)

        if not comment.is_deleted and serializer.is_valid() and (comment.author == request.user or request.user.profile.HasPermission('delete_comment')):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif comment.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_400_BAD_REQUEST)

class VoteDetail(APIView):
    def get(self, request):
        vote_target_id   = request.GET.get('id')
        vote_target_type = request.GET.get('type')

        if not vote_target_type:
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
        data['author'] = request.user.id

        id = request.POST.get('id', False)
        type = request.POST.get('type', False)
        direction = request.POST.get('direction', False)

        content_type_mapping = {"comment": ContentType.objects.get_for_model(Comment).id,
                                "image": ContentType.objects.get_for_model(Image).id,
                                "video": ContentType.objects.get_for_model(Video).id}

        if type and id and Saiba.utils.is_valid_direction(direction):
            past_vote = Vote.objects.filter(target_id=id, target_content_type=content_type_mapping[type],
                                            author=request.user).first()

            if past_vote:
                if int(past_vote.direction) != int(direction):
                    past_vote.direction = direction
                    past_vote.save()
                else:
                    past_vote.direction = 0
                    past_vote.save()
            else:
                vote_target_type = type
                data["target_id"] = id

                data["target_content_type"] = content_type_mapping[type]

        serializer = VoteSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            if type == "comment":
                comment = Comment.objects.filter(id=id).first()
                comment.update_points()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

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
                video           = get_object_or_404(Video, id=comment_target_id)
                target_type_id  = ContentType.objects.get_for_model(Video).id
                target_id = video.id
            elif comment_target_type == "profile" and comment_target_id:
                profile         = get_object_or_404(Profile, id=comment_target_id)
                target_type_id  = ContentType.objects.get_for_model(Profile).id
                target_id = profile.user.id

            comments = Comment.objects.filter(target_id=target_id, target_content_type=target_type_id,
                                              is_deleted=False).order_by('-creation_date')

        for comment in comments:
            comment_type_id = ContentType.objects.get_for_model(Comment).id
            comment.points = (Vote.objects.filter(target_id=comment.pk,
                                                target_content_type=comment_type_id).aggregate(Sum('direction')))['direction__sum']
            for reply in replies:
                reply.points = (Vote.objects.filter(target_id=reply.pk, 
                                              target_content_type=reply_type_id).aggregate(Sum('direction')))['direction__sum']

        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(comments, request)

        serializer = CommentSerializer(result_page, many=True, context={"reply_limit":reply_limit})
        return paginator.get_paginated_response(serializer.data)        

class PointsDetail(APIView):
    def get(self, request):
        vote_target_id   = request.GET.get('id')
        vote_target_slug = request.GET.get('slug')
        vote_target_type = request.GET.get('type')

        target_type_id = None
        target_id      = None

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

class TrendingDetail(APIView):
    def get(self, request, tg_type = None):
        trending_type = request.GET.get('type') or tg_type
        gallery = request.GET.get('gallery') or None # ID of the entry whose the gallery will be queried
        offset = request.GET.get('offset') or 0
        step = request.GET.get('step') or 20

        step = int(step)
        offset = int(offset)

        if trending_type:
            if trending_type == "entry":
                entries = Entry.objects.filter(hidden=False).annotate(total_points=Sum('trending_votes__points')).order_by('-total_points')[offset:offset+step]
                serializer = EntrySerializer(entries, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            elif trending_type == "gallery":
                galleries = Entry.objects.filter(hidden=False).annotate(gallery_points=Sum('images__trending_points')).order_by('-gallery_points')[offset:offset+step]
                serializer = EntrySerializer(galleries, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            elif trending_type == "image":
                if gallery:
                    images = Image.objects.filter(hidden=False).filter(entry=int(gallery)).annotate(total_points=Sum('trending_votes__points')).order_by('-total_points')[offset:offset+step]
                else:
                    images = Image.objects.annotate(total_points=Sum('trending_votes__points')).order_by('-total_points')[offset:offset+step]
                serializer = ImageSerializer(images, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            elif trending_type == "video":
                videos = Video.objects.filter(hidden=False).annotate(total_points=Sum('trending_votes__points')).order_by('-total_points')[offset:offset+step]
                serializer = VideoSerializer(videos, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class SearchDetail(APIView):
    def get(self, request):
        search_text = request.GET.get('search')
        search_type = request.GET.get('type')

        if search_text and search_type:
            if search_type == "entry":
                entries = None

                if request.user.is_staff:
                    entries = Entry.objects.filter(title__contains=search_text)[:20]
                else:
                    entries = Entry.objects.filter(title__contains=search_text, hidden=False)[:20]
                    
                serializer = EntrySerializer(entries, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    
class PreviewDetail(APIView):
    def post(self, request):
        content = request.POST.get('content')

        if content:
            result = Saiba.parser.parse(content)
            return Response(result, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)

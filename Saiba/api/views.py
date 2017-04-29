from django.db.models import Sum
from django.shortcuts import render, get_object_or_404
from django.views import generic
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from profile.models import Profile
from home.models import SaibaSettings
from entry.models import Entry, Revision
from entry.serializers import EntrySerializer, RevisionSerializer
from feedback.models import Comment, Vote
from feedback.serializers import CommentSerializer, VoteSerializer, PointsSerializer
from gallery.models import Image, Video
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from rest_framework.pagination import PageNumberPagination
import Saiba.utils
import Saiba.saibadown, textile

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
        data['author'] = request.user.id;

        serializer = EntrySerializer(data=data)
        
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
        data['author'] = request.user.id;

        types_map = { "comment": Comment, "image": Image, "video": Video, "entry": Entry, "profile": Profile }
        target_type = types_map[data["type"]];

        data["target_content_type"] = ContentType.objects.get_for_model(target_type).id
        data["target_id"]           = data['id']

        serializer = CommentSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            if target_type == Entry:
                trending_weight = int(SaibaSettings.objects.get(type="trending_weight_comment").value)
                entry = Entry.objects.get(id=data['id'])
                entry.trending_points += trending_weight # Someone commented, so the entry should get trend points
                entry.save(update_fields=['trending_points'])
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

        if not comment.is_deleted and serializer.is_valid() and comment.author == request.user:
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
        data['author'] = request.user.id;

        id = request.POST.get('id', False)
        type = request.POST.get('type', False)
        direction = request.POST.get('direction', False)

        content_type_mapping = {"comment": ContentType.objects.get_for_model(Comment).id,
                                "image": ContentType.objects.get_for_model(Image).id,
                                "video": ContentType.objects.get_for_model(Video).id}

        if type and id and Saiba.utils.is_valid_direction(direction):
            past_vote = Vote.objects.filter(target_id=id, target_content_type=content_type_mapping[type], author=request.user).first()

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

            comments = Comment.objects.filter(target_id=target_id, 
                                              target_content_type=target_type_id, is_deleted=False).order_by('-creation_date')

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
        #return Response(status=status.HTTP_400_BAD_REQUEST)

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
    def get(self, request, type = None):
        trending_type = request.GET.get('type') or type

        if trending_type:
            if trending_type == "entry":
                entries = Entry.objects.all().order_by('-trending_points')[:20]
                serializer = EntrySerializer(entries, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            elif trending_type == "gallery":
                galleries = Entry.objects.filter(hidden=False).annotate(gallery_points=Sum('images__trending_points')).order_by('-gallery_points')[:20]
                serializer = EntrySerializer(galleries, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            elif trending_type == "image":
                image = Image.objects.all().order_by('-trending_points')[:20]
                serializer = ImageSerializer(image, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class SearchDetail(APIView):
    def get(self, request):
        search_text = request.GET.get('search')
        search_type = request.GET.get('type')

        if search_text and search_type:
            if search_type == "entry":
                entries = Entry.objects.filter(title__contains=search_text, hidden=False)[:20]
                serializer = EntrySerializer(entries, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    
class PreviewDetail(APIView):
    def post(self, request):
        content = request.POST.get('content')

        if content:
            result = Saiba.saibadown.parse(textile.textile(content))
            return Response(result, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)
from django.contrib import admin
from .models import Comment, CommentVote, ImageVote, VideoVote

admin.site.register(Comment)
admin.site.register(CommentVote)
admin.site.register(ImageVote)
admin.site.register(VideoVote)
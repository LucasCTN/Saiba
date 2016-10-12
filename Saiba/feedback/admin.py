from django.contrib import admin
from .models import EntryComment, ImageComment, CommentVote, ImageVote, VideoVote

admin.site.register(EntryComment)
admin.site.register(ImageComment)
admin.site.register(CommentVote)
admin.site.register(ImageVote)
admin.site.register(VideoVote)
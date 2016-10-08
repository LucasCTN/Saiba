from django.contrib import admin
from .models import EntryComment, ImageComment, EntryCommentVote, ImageVote, VideoVote

admin.site.register(EntryComment)
admin.site.register(ImageComment)
admin.site.register(EntryCommentVote)
admin.site.register(ImageVote)
admin.site.register(VideoVote)
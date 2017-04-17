from django.contrib import admin
from .models import Comment, Vote

admin.site.register(Comment)
admin.site.register(Vote)
from django.contrib import admin
from .models import Comment, Vote, Action

admin.site.register(Comment)
admin.site.register(Vote)
admin.site.register(Action)
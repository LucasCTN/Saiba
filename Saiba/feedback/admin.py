from django.contrib import admin
from .models import Comment, Vote, Action, View

admin.site.register(Comment)
admin.site.register(Vote)
admin.site.register(Action)
admin.site.register(View)
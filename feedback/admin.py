from django.contrib import admin
from .models import Comment, Vote, Action, View
from .models import Comment, Vote, Action, TrendingVote

admin.site.register(Comment)
admin.site.register(Vote)
admin.site.register(Action)
admin.site.register(View)
admin.site.register(TrendingVote)
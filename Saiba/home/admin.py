from django.contrib import admin
from .models import Post, Label, Tag

admin.site.register(Post)
admin.site.register(Label)
admin.site.register(Tag)
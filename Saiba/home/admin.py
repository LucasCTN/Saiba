from django.contrib import admin
from .models import Post, Label, Tag, SaibaSettings

admin.site.register(Post)
admin.site.register(Label)
admin.site.register(Tag)
admin.site.register(SaibaSettings)
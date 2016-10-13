from django.contrib import admin
from .models import Entry, Revision, Status, Category

admin.site.register(Entry)
admin.site.register(Revision)
admin.site.register(Status)
admin.site.register(Category)

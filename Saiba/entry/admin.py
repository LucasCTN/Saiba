from django.contrib import admin
from .models import Entry, Revision, Status, Category, EntryRedirect

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Revision)
admin.site.register(Status)
admin.site.register(Category)
admin.site.register(EntryRedirect)
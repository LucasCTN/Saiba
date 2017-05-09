from django.contrib import admin
from .models import UserPermission, UserGroup

# Register your models here.
admin.site.register(UserPermission)
admin.site.register(UserGroup)

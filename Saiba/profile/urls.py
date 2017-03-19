from django.conf.urls import url
from . import views

app_name = 'profile'

urlpatterns = [
    url(r'^(?P<name_slug>[\w-]+)/$', views.detail, name='detail'),
    url(r'^(?P<name_slug>[\w-]+)/editoria', views.editorships, name='editorships'),
    url(r'^(?P<name_slug>[\w-]+)/imagens', views.images, name='images'),
    url(r'^(?P<name_slug>[\w-]+)/videos', views.videos, name='videos'),
]

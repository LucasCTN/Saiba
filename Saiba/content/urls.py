from django.conf.urls import url
from . import views

app_name = 'content'

urlpatterns = [
    url(r'^blog/nova-postagem/$', views.bpost_create, name='bpost_create'),
    url(r'^blog/(?P<bpost_slug>[\w-]+)/$', views.bpost_detail, name='bpost_detail'),
    url(r'^blog/(?P<bpost_slug>[\w-]+)/editar/$', views.bpost_edit, name='bpost_edit'),
]

from django.conf.urls import url
from . import views

app_name = 'gallery'

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^enviar-imagem/$', views.upload_image, name='upload_image'),
    url(r'^enviar-video/$', views.upload_video, name='upload_video'),
    url(r'^imagem/(?P<image_id>[0-9]+)/$', views.image_detail, name='image_detail'),
    url(r'^video/(?P<video_id>[0-9]+)/$', views.video_detail, name='video_detail'),
    url(r'^pesquisar-tags/$', views.search_tags, name='search_tags'),
    url(r'^pesquisar-entradas/$', views.search_entries, name='search_entries'),
]

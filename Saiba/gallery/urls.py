from django.conf.urls import url
from . import views

app_name = 'gallery'

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^enviar-imagem/$', views.upload_image, name='upload_image'),
    url(r'^enviar-video/$', views.upload_video, name='upload_video'),
    url(r'^imagem/(?P<image_id>[0-9]+)/$', views.image_detail, name='image_detail'),
]

from django.conf.urls import url
from . import views

app_name = 'staff'

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^create-post$', views.create_post, name = 'create_post'),
]
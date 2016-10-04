from django.conf.urls import url
from . import views

app_name = 'profile'

urlpatterns = [
    url(r'^(?P<name_slug>[\w-]+)/$', views.index, name='index'),
]

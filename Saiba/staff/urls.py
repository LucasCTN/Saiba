from django.conf.urls import url
from . import views

app_name = 'staff'

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
]
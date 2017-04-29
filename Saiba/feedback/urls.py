from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'feedback'

urlpatterns = [
    url(r'^comment_page/$', views.comment_page, name='comment_page'),
]
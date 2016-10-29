from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'api'

urlpatterns = [
    url(r'^v1/artigos/(?P<slug>[\w-]+)/$', views.EntryDetail.as_view(), name='api_article'),
    url(r'^v1/historicos/(?P<slug>[\w-]+)/$', views.HistoricDetail.as_view(), name='api_historic'),
    url(r'^v1/comment/$', views.CommentDetail.as_view(), name='api_comments'),
    url(r'^v1/comment_page/$', views.CommentPageDetail.as_view(), name='api_comment_page'),
    url(r'^v1/vote/$', views.VoteDetail.as_view(), name='api_vote'),
]
from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^v1/artigos/(?P<slug>[\w-]+)/$', views.EntryDetail.as_view(), name='api_article'),
    url(r'^v1/historicos/(?P<slug>[\w-]+)/$', views.HistoricDetail.as_view(), name='api_historic'),
    url(r'^v1/comentarios/(?P<slug>[\w-]+)/$', views.CommentDetail.as_view(), name='api_comments'),
    url(r'^v1/votar/$', views.CommentVote.as_view(), name='api_vote'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
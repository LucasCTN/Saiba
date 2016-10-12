from django.conf.urls import url
from . import views

app_name = 'entry'

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^nova-entrada/', views.create_entry, name='create_entry'),
    url(r'^(?P<entry_slug>[\w-]+)/$', views.detail, name='detail'),
    url(r'^(?P<entry_slug>[\w-]+)/historico$', views.history, name='history'),
    url(r'^(?P<entry_slug>[\w-]+)/editar', views.edit, name='edit'),
    url(r'^(?P<entry_slug>[\w-]+)/revisoes/(?P<revision_id>[0-9]+)', views.revision, name='revision'),
    url(r'^(?P<entry_slug>[\w-]+)/editoria$', views.editorship, name='editorship'),
]

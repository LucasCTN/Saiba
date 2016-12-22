from django.conf.urls import url
from . import views

app_name = 'home'

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^entrar/$', views.user_login, name = 'login'),
    url(r'^sair/$', views.user_logout, name = 'logout'),
    url(r'^registrar/$', views.user_register, name = 'register'),
    url(r'^pesquisar/$', views.search, name = 'search'),
    url(r'^pesquisar-ajax/$', views.search_results, name = 'search_results'),
]
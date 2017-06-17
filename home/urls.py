from django.conf.urls import url
from . import views

app_name = 'home'

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^entrar/$', views.user_login, name = 'login'),
    url(r'^sair/$', views.user_logout, name = 'logout'),
    url(r'^registrar/$', views.user_register, name = 'register'),
    url(r'^pesquisar/$', views.page_search, name = 'page_search'),
    url(r'^pesquisar-navbar/$', views.navbar_search, name = 'navbar_search'),
    url(r'^pesquisar-entrada/$', views.search_entry, name = 'search_entry'),
    url(r'^pesquisar-tag/$', views.search_tag, name='search_tag'),
    url(r'^trending/$', views.trending_page, name='trending_page'),
    url(r'^trending_list/$', views.trending_list, name='api_trending_list'),
    url(r'^imagens-populares/$', views.popular_images, name='popular_images'),
    url(r'^teapot/$', views.custom_418, name='custom_418'),
    url(r'^ativar/(?P<username_slug>[\w-]+)/(?P<token_code>.+|)/$',
        views.email_activation, name='email_activation'),
    url(r'^checar-registro/$', views.email_check_activation, name='email_check_activation'),
]

from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^index/$', views.index, name='index'),
    url(r'^user_index/$', views.user_index, name='user_index'),
    url(r'^user_login/$', views.user_login, name='user_login'),
    url(r'^user_logout/$', views.user_logout, name='user_logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^user_update/$', views.user_update, name='user_update'),
    url(r'^user_pass/$', views.user_pass, name='user_pass'),
    url(r'^user_list/$', views.user_list, name='user_list'),
    url(r'^user_update/$', views.user_update, name='user_update'),
    url(r'^article_add/$', views.article_add, name='article_add'),
    url(r'^article_update/(?P<a_id>\d+)/$', views.article_update, name='article_update'),

    # url(r'^love_add/(?P<art_id>\d+)/$', views.love_add, name='love_add'),
    url(r'^article_delete/(?P<a_id>\d+)/$', views.article_delete, name='article_delete'),
    url(r'^article_detail/(?P<a_id>\d+)/$', views.article_detail, name='article_detail'),
    url(r'^detail/(?P<a_id>\d+)$', views.detail, name='detail'),
    url(r'^article_list/$', views.article_list, name='article_list'),
    url('^creataCode/$', views.creataCode, name='creataCode'),

]

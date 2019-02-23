from django.conf.urls import url

from . import views


urlpatterns = [

    url('^news/$', views.news, name='news'),
    url('^alter/$', views.alter, name='alter'),
    url('^address/$', views.address, name='address'),
    url('^add/$', views.add, name='add'),
    url('^del1/$', views.del1, name='del1'),
    url('^defo1/$', views.defo1, name='defo1'),










]
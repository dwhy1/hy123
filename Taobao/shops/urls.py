from django.conf.urls import url

from . import views


urlpatterns = [

    url('^shop1/$', views.shop1, name='shop1'),
    url('^off/$', views.off, name='off'),
    url('^open/$', views.open, name='open'),
    url('^thing/$', views.thing, name='thing'),

]
from django.conf.urls import url

from . import views


urlpatterns = [
    url('^index/$', views.index, name='index'),

    # url('^index1/$', views.index1, name='index1'),
    url('^shop/$', views.shop, name='shop'),
    url('^cart/$', views.cart, name='cart'),
    url('^good1/$', views.good1, name='good1'),
    url('^shop/$', views.shop, name='shop'),
    url('^del1/$', views.del1, name='del1'),

]
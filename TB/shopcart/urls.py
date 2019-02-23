from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^(?P<g_id>\d+)/(?P<num>\d+)/add_shopcart/$',views.add_shopcart,name='add_shopcart'),
    url(r'^(?P<g_id>\d+)/(?P<num>\d+)/shopcart_update/$',views.shopcart_update,name='shopcart_update'),
    url(r'^shopcart_info/$',views.shopcart_info,name='shopcart_info'),
    url(r'^(?P<p_id>\d+)/del_shopcart/$',views.del_shopcart,name='del_shopcart'),
]
from django.conf.urls import url
from . import views



urlpatterns=[
    url(r'^add_type/$',views.add_type,name='add_type'),
    url(r'^(?P<s_id>\d+)/add_goods/$',views.add_goods,name='add_goods'),
    url(r'^(?P<g_id>\d+)/update_goods/$',views.update_goods,name='update_goods'),
    url(r'^(?P<s_id>\d+)/goods_list/$',views.goods_list,name='goods_list'),
    url(r'^(?P<g_id>\d+)/goods_info/$',views.goods_info,name='goods_info'),
    url(r'^select2/$',views.select2,name='select2'),

]
from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^index/$', views.index, name='index'),  # 首页
    url(r'^detail/(?P<goods_id>\d+)/$', views.detail, name='detail'),  # 详情页
    url(r'list/(?P<type_id>\d+)/(?P<page>\d+)$', views.list, name='list'),  # 列表页
    url(r'^(?P<s_id>\d+)/goods_list/$', views.goods_list, name='goods_list'),  # 店铺商品列表页
    url(r'^(?P<g_id>\d+)/update_goods/$', views.update_goods, name='update_goods'),  # 商品修改页面

]

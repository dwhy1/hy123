from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^CartAdd$', views.CartAdd, name='CartAdd'),  # 购物车记录添加
    url(r'^cartInfo$', views.cartInfo, name='cartInfo'),  # 购物车页面显示
    url(r'^update$', views.update, name='update'),  # 购物车记录更新
    url(r'^delete$', views.delete, name='delete'),  # 购物车删除纪录

]

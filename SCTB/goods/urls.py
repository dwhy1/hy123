from django.conf.urls import url

from . import views


urlpatterns = [
    url('^login/$', views.login, name='login'),
    url('^register/$', views.register, name='register'),
    url('^creataCode/$', views.creataCode, name='creataCode'),
    url('^index/$', views.index, name='index'),
    # 店铺路由
    url('^shop1/$', views.shop1, name='shop1'),
    url('^off/$', views.off, name='off'),
    url('^open/$', views.open, name='open'),
    url('^thing/$', views.thing, name='thing'),
    # 用户路由
    url('^news/$', views.news, name='news'),
    url('^alter/$', views.alter, name='alter'),
    url('^address/$', views.address, name='address'),
    url('^add/$', views.add, name='add'),
    url('^del1/$', views.del1, name='del1'),
    url('^defo1/$', views.defo1, name='defo1'),
    # 商品路由
    url('^shop/$', views.shop, name='shop'),
    url('^cart/$', views.cart, name='cart'),
    url('^good1/$', views.good1, name='good1'),
    url('^debut/$', views.debut, name='debut'),
    url('^rem/$', views.rem, name='rem'),
    url('^shopcart_info/$', views.shopcart_info, name='shopcart_info'),
    url('^del_shopcart/$', views.del_shopcart, name='del_shopcart'),

    url('^order_confirm/$', views.order_confirm, name='order_confirm'),









]
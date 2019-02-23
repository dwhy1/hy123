from . import views
from django.conf.urls import url


urlpatterns=[
    url(r'^order_confirm/$',views.order_confirm,name='order_confirm'),
    url(r'^order_done/$',views.order_done,name='order_done'),
    url(r'^order_list/$',views.order_list,name='order_list'),
    url(r'^(?P<o_id>\d+)/del_order/$',views.del_order,name='del_order'),
    url(r'^(?P<o_id>\d+)/order_detail/$',views.order_detail,name='order_detail'),
]
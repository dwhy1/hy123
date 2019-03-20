from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^OrderPlace$', views.OrderPlace, name='OrderPlace'),  # 提交订单页面显示
    url(r'^OrderCommit$', views.OrderCommit, name='OrderCommit'),  # 订单创建
    url(r'^OrderPlay$', views.OrderPlay, name=' OrderPlay'),  # 订单支付
    # url(r'^check$', CheckPayView.as_view(), name='check'),  # 查询支付交易结果
    # url(r'^comment/(?P<order_id>.+)$', CommentView.as_view(), name='comment'),  # 订单评论

]

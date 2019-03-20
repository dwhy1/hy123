from django.conf.urls import url

from . import views

urlpatterns = [

    # url(r'^index/$', views.index, name='index'),
    url(r'^user_login/$', views.user_login, name='user_login'),
    url(r'^user_logout/$', views.user_logout, name='user_logout'),
    url(r'^register/$', views.register, name='register'),
    url('^creataCode/$', views.creataCode, name='creataCode'),  # 验证码
    url(r'^user_info/$', views.user_info, name='user_info'),  # 用户中心-信息页
    url(r'^user_add/$', views.user_add, name='user_add'),  # 用户中心-完善信息页
    url(r'^user_pass/$', views.user_pass, name='user_pass'),  # 用户中心-密码修改页
    url(r'^user_order/(?P<page>\d+)/$', views.user_order, name='user_order'),  # 用户中心——订单详情页

    url(r'^user_address/$', views.user_address, name='user_address'),  # 用户中心—地址页
    url(r'^addr_update/$', views.addr_update, name='addr_update'),  # 用户中心-地址修改
    url(r'^(?P<addr_id>\d+)/addr_del/$', views.addr_del, name='addr_del'),  # 用户中心-地址删除

]

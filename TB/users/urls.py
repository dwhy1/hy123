from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^index/$', views.index,name='index'),
    url(r'^register/$', views.register,name='register'),
    url(r'^logins/$', views.logins,name='logins'),
    url(r'^logouts/$', views.logouts,name='logouts'),
    url(r'^reg_email/$', views.reg_email,name='reg_email'),
    url(r'^get_code/$', views.get_code,name='get_code'),
    url(r'^checkname/$', views.checkname,name='checkname'),
    url(r'^checkemail/$', views.checkemail,name='checkemail'),
    url(r'^userinfo/$', views.userinfo,name='userinfo'),
    url(r'^changeinfo/$', views.changeinfo,name='changeinfo'),
    url(r'^changeavatar/$', views.changeavatar,name='changeavatar'),
    url(r'^changepwd/$', views.changepwd,name='changepwd'),
    #地址
    url(r'^add_addr/$', views.add_addr,name='add_addr'),
    url(r'^addr_update/$', views.addr_update,name='addr_update'),
    url(r'^(?P<addr_id>\d+)/addr_del/$', views.addr_del,name='addr_del'),

    url(r'^$',views.index,name='index'),

]

from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^add/$',views.add,name='add'),
    url(r'^store_list/$',views.store_list,name='store_list'),
    url(r'^(?P<s_id>\d+)/storeinfo/$',views.storeinfo,name='storeinfo'),

    url(r'^(?P<s_id>\d+)/update_store/$',views.update_store,name='update_store'),

]
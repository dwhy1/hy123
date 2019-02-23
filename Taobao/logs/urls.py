from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^login/$',views.login,name='login'),

    url('^register/$', views.register, name='register'),

    url('^creataCode/$',views.creataCode,name='creataCode'),


]
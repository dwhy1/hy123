from django.conf.urls import url

from . import views


urlpatterns = [

    url(r'post-comment/(\d+)/$', views.post_comment, name='post_comment'),

]
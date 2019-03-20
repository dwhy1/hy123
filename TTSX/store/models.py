from django.db import models
from django.contrib.auth.models import User


class Store(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name='店铺名字')
    cover = models.ImageField(upload_to='static/img/store/', default='static/img/store/default.jpg', verbose_name='店铺图片')
    intro = models.CharField(max_length=255, default='这家伙很懒，什么都没写', verbose_name='店铺介绍')
    opentime = models.DateTimeField(auto_now_add=True, verbose_name='开店时间')
    status = models.IntegerField(default=1, verbose_name='店铺状态', null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='店铺主人')









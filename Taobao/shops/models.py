from django.db import models

from users.models import User
# Create your models here.


# 店铺信息
class Store(models.Model):
    id = models.AutoField(primary_key=True,verbose_name='id')
    name = models.CharField(max_length=225,verbose_name='店铺名称')
    cover = models.ImageField(verbose_name='店铺封面',upload_to='static/img/shops/', default='static/img/shops/1.jpg')
    intro = models.CharField(verbose_name='店铺描述',max_length=255, null=True, blank=True)
    opener_time = models.DateTimeField(verbose_name='开店时间', auto_now_add=True, editable=True)
    status = models.CharField(verbose_name='店铺状态',max_length=255)
    users = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='所属用户')


from django.db import models
from store.models import Store
# Create your models here.


# 商品类型
class GoodsType(models.Model):
    id = models.AutoField(primary_key=True)
    gt_name = models.CharField(max_length=50, verbose_name='商品类型')
    gt_desc = models.CharField(max_length=255, default='这家伙太懒了。。。。', verbose_name='类型描述')
    gt_parent = models.ForeignKey('self', null=True, blank=True)


# 商品信息
class Goods(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='商品id')
    name = models.CharField(max_length=50, blank=False, null=False, verbose_name='商品名字')
    price = models.FloatField(verbose_name='商品价格')
    stock = models.IntegerField(verbose_name='商品库存')
    count = models.IntegerField(default=0, verbose_name='商品销量')
    status = models.IntegerField(default=1, verbose_name='商品状态')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='上架时间')
    desc = models.CharField(max_length=255, verbose_name='商品介绍')
    goods_type = models.ForeignKey(GoodsType, on_delete=models.CASCADE)
    goods_store = models.ForeignKey(Store, on_delete=models.CASCADE)


# 商品图片
class GoodsImg(models.Model):
    id = models.AutoField(primary_key=True)
    path = models.ImageField(upload_to='static/goods/img/', default='static/goods/img/default.jpg')
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name='所属商品')
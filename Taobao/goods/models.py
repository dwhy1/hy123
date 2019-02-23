from django.db import models

from shops.models import Store
# Create your models here.


# 商品类型
class GoodsType(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='id')
    gt_name = models.CharField(verbose_name='类型名称',max_length=255)
    cover = models.ImageField(verbose_name='图片', upload_to='static/img/goods/', null=True, blank=True)
    gt_desc = models.CharField(verbose_name='类型描述',max_length=255, null=True, blank=True)


# 商品信息
class Goods(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='id')
    name = models.CharField(verbose_name='商品名称',max_length=255)
    price = models.CharField(verbose_name='商品单价',max_length=255)
    stock = models.CharField(verbose_name='商品库存',max_length=255)
    count = models.CharField(verbose_name='销售数量',max_length=255)
    img = models.ImageField(verbose_name='商品图片',upload_to='static/img/goods/',null=True,blank=True)
    add_time = models.DateTimeField(verbose_name='上架时间', auto_now_add=True, editable=True)
    desc = models.CharField(verbose_name='商品描述',max_length=255, null=True, blank=True)
    goods_detail_type =models.ForeignKey(GoodsType, on_delete=models.CASCADE, verbose_name='所属类型')
    goods_store = models.ForeignKey(Store, on_delete=models.CASCADE, verbose_name='所属店铺')

# 商品图片
class GoodsImg(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='id')
    path = models.ImageField(verbose_name='商品图片',upload_to='static/img/goods/',null=True,blank=True)
    status = models.CharField(max_length=255)
    goods =  models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name='所属商品')


from django.db import models
from goods.models import Goods
from django.contrib.auth.models import User


class ShopCart(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='购物车id')
    num = models.IntegerField(verbose_name='购买数量')
    subtotal = models.FloatField(verbose_name='小计')
    time = models.DateTimeField(auto_now_add=True)
    goods = models.ForeignKey(Goods, verbose_name='购物车商品')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Orders(models.Model):
    id = models.AutoField(primary_key=True, )
    time = models.DateTimeField(auto_now_add=True, )
    total = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    addr = models.CharField(max_length=255, null=False, )
    remark = models.CharField(max_length=255, blank=True)
    status = models.BooleanField(default=True)


class OrdersItem(models.Model):
    id = models.AutoField(primary_key=True)
    goodsimg = models.ImageField(upload_to='static/orders/img')
    goodsname = models.CharField(max_length=50)
    goodsnum = models.IntegerField()
    goodsprice = models.FloatField()
    goodssubtotal = models.FloatField()
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)

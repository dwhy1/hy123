from django.db import models

from goods.models import Goods
# Create your models here.
from django.contrib.auth.models import User

# 类的管理器
class UsersManager(models.Manager):
    pass


# 用户
class User1(models.Model):
    id = models.AutoField(primary_key=True,verbose_name='id')
    username = models.CharField(verbose_name='用户姓名',max_length=255)
    userpass = models.CharField(verbose_name='用户密码',max_length=255)
    nickname = models.CharField(verbose_name='用户昵称',max_length=255)
    age = models.CharField(verbose_name='用户年龄',max_length=255)
    gender = models.CharField(verbose_name='用户性别',max_length=255)
    header = models.ImageField(verbose_name='用户头像',upload_to='static/img/users/', null=True, blank=True)
    phone = models.CharField(verbose_name='联系电话',max_length=12)
    email = models.CharField(verbose_name='电子邮箱',max_length=255, null=True, blank=True)
    regist_time = models.DateTimeField(verbose_name='注册时间', auto_now_add=True, editable=True)
    last_login_time = models.DateTimeField(verbose_name='上次登录时间', auto_now_add=True, editable=True)
    status = models.CharField(verbose_name='用户状态',max_length=255)
    usermanager = UsersManager()


# 收货地址：
class Address(models.Model):
    id = models.AutoField(primary_key=True,verbose_name='id')
    recv_name = models.CharField(verbose_name='收货人姓名',max_length=255)
    recv_phone = models.CharField(verbose_name='收货人联系方式',max_length=255)
    provice = models.CharField(verbose_name="省份",max_length=255)
    city = models.CharField(verbose_name='市区',max_length=255)
    country = models.CharField(verbose_name='县区',max_length=255)
    street = models.CharField(verbose_name='街道',max_length=255)
    desc = models.CharField(verbose_name='详细描述',max_length=255, null=True, blank=True)
    status = models.CharField(verbose_name='默认地址',max_length=255)
    users = models.ForeignKey(User1, on_delete=models.CASCADE, verbose_name='所属用户')


# 购物车信息：
class ShopCart(models.Model):
    id = models.AutoField(primary_key=True,verbose_name='id')
    # 商品也是外键
    goods = models.ForeignKey(Goods,verbose_name='购物车商品',on_delete=models.CASCADE)
    count = models.CharField(verbose_name='数量数量',max_length=255)
    add_time = models.DateTimeField(verbose_name='商品添加时间',auto_now_add=True, editable=True)
    subtotal = models.CharField(verbose_name='总计金额',max_length=255)
    users = models.ForeignKey(User1, on_delete=models.CASCADE, verbose_name='所属用户')


# 订单：
class Order(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='id')
    order_time = models.DateTimeField(verbose_name='下单时间', auto_now_add=True, editable=True)
    recv_name = models.CharField(verbose_name='收货人',max_length=255)
    recv_address = models.CharField(verbose_name='收货地址',max_length=255)
    recv_phone = models.CharField(verbose_name='联系方式',max_length=255)
    recv_remark = models.CharField(verbose_name='备注信息',max_length=255, null=True, blank=True)
    totale = models.CharField(verbose_name='总计金额',max_length=255)
    users = models.ForeignKey(User1, on_delete=models.CASCADE, verbose_name='所属用户')


# 订单单项：
class OrderItem(models.Model):
    id = models.AutoField(primary_key=True,verbose_name='id')
    oi_goods_id = models.CharField(verbose_name='订单编号',max_length=255)
    oi_goods_name = models.CharField(verbose_name='订单商品名称',max_length=255)
    oi_goods_price = models.CharField(verbose_name='订单商品金额',max_length=255)
    oi_goods_count = models.CharField(verbose_name='订单商品数量',max_length=255)
    deal_price = models.CharField(verbose_name='成交价格',max_length=255)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='所属订单')




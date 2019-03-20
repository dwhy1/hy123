from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User
from django.urls import reverse


class UserInfo(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='用户标识')
    age = models.IntegerField(default=18, verbose_name='用户年龄')
    gender = models.CharField(max_length=10, default='男', verbose_name='用户性别')
    nickname = models.CharField(max_length=10, verbose_name='用户昵称')
    headers = models.ImageField(verbose_name='用户头像', upload_to='static/img/users/', default='static/img/users/d1.jpg')
    # 一对一外键
    user = models.OneToOneField(User, on_delete=models.CASCADE)



class AddressManager(models.Manager):
    '''


    地址模型管理器类


    '''

    # 改变原有查询的结果集：all()
    # 封装方法：用户操作模型类对应的数据表（增删改查）
    def get_default_address(self, user):
        '''获取用户默认收货地址'''
        try:
            address = self.get(user=user, is_default=True)
        except self.model.DoesNotExist:
            # 不存在默认收货地址
            address = None

        return address


class Address(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='dizhi_id')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='所属用户')
    receiver = models.CharField(max_length=20, verbose_name='收件人')
    addr = models.CharField(max_length=256, verbose_name='收件地址')
    zip_code = models.CharField(max_length=6, null=True, verbose_name='邮政编码')
    phone = models.CharField(max_length=11, verbose_name='联系电话')
    intro = models.CharField(max_length=255, verbose_name='详细描述')
    is_default = models.BooleanField(default=False, verbose_name='是否默认')

    objects = AddressManager()

    class Meta:
        db_table = 'df_address'
        verbose_name = '地址'
        verbose_name_plural = verbose_name

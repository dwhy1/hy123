from django.db import models


from tinymce.models import HTMLField
from django.contrib.auth.models import User


class Users(models.Model):
    age = models.IntegerField(default=18)
    gender = models.CharField(max_length=10, default='男', verbose_name='用户性别')
    user = models.OneToOneField(User)


class Article(models.Model):
    id = models.AutoField(primary_key=True,verbose_name='文章主键')
    title = models.CharField(max_length=255,verbose_name='文章标题')
    text = HTMLField(verbose_name='文章内容')
    author = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='作者')










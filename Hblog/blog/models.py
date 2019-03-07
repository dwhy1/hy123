from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User
from django.urls import reverse


class Users(models.Model):
    age = models.IntegerField(default=18)
    gender = models.CharField(max_length=10, default='男', verbose_name='用户性别')
    nickname = models.CharField(max_length=10,  verbose_name='用户昵称')
    headers = models.ImageField(verbose_name='用户头像', upload_to='static/img/users/', default='static/img/users/tx5.jpg')
    user = models.OneToOneField(User)


class Article(models.Model):
    id = models.AutoField(primary_key=True,verbose_name='文章主键')
    title = models.CharField(max_length=255,verbose_name='文章标题')
    content =models.TextField(verbose_name='文章内容')
    reamark = models.CharField(max_length=255, verbose_name='文章摘要')
    starTime = models.DateTimeField(verbose_name='发表时间', auto_now_add=True)
    updateTime = models.DateTimeField(verbose_name='更新时间', auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')

    # 获取文章地址
    def get_absolute_url(self):
        return reverse('blog:detail', args=[self.id])










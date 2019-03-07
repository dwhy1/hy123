# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-03-06 08:49
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='文章主键')),
                ('title', models.CharField(max_length=255, verbose_name='文章标题')),
                ('content', models.TextField(verbose_name='文章内容')),
                ('reamark', models.CharField(max_length=255, verbose_name='文章摘要')),
                ('starTime', models.DateTimeField(auto_now_add=True, verbose_name='发表时间')),
                ('updateTime', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='作者')),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.IntegerField(default=18)),
                ('gender', models.CharField(default='男', max_length=10, verbose_name='用户性别')),
                ('nickname', models.CharField(max_length=10, verbose_name='用户昵称')),
                ('headers', models.ImageField(default='static/img/users/tx5.jpg', upload_to='static/img/users/', verbose_name='用户头像')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
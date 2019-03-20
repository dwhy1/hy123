# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-03-19 03:35
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
            name='Store',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, verbose_name='店铺名字')),
                ('cover', models.ImageField(default='static/img/store/default.jpg', upload_to='static/img/store/', verbose_name='店铺图片')),
                ('intro', models.CharField(default='这家伙很懒，什么都没写', max_length=255, verbose_name='店铺介绍')),
                ('opentime', models.DateTimeField(auto_now_add=True, verbose_name='开店时间')),
                ('status', models.IntegerField(default=1, verbose_name='店铺状态')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='店铺主人')),
            ],
        ),
    ]

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
        ('user', '0001_initial'),
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderGoods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=1, verbose_name='商品数目')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='商品价格')),
                ('comment', models.CharField(default='', max_length=256, verbose_name='评论')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '订单商品',
                'verbose_name_plural': '订单商品',
                'db_table': 'df_order_goods',
            },
        ),
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('order_id', models.CharField(max_length=128, primary_key=True, serialize=False, verbose_name='订单id')),
                ('pay_method', models.SmallIntegerField(choices=[(1, '货到付款'), (2, '微信支付'), (3, '支付宝'), (4, '银联支付')], default=3, verbose_name='支付方式')),
                ('total_count', models.IntegerField(default=1, verbose_name='商品数量')),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='商品总价')),
                ('transit_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='订单运费')),
                ('order_status', models.SmallIntegerField(choices=[(1, '待支付'), (2, '待发货'), (3, '待收货'), (4, '待评价'), (5, '已完成')], default=1, verbose_name='订单状态')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('trade_no', models.CharField(default='', max_length=128, verbose_name='支付编号')),
                ('addr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Address', verbose_name='地址')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '订单',
                'verbose_name_plural': '订单',
                'db_table': 'df_order_info',
            },
        ),
        migrations.AddField(
            model_name='ordergoods',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.OrderInfo', verbose_name='订单'),
        ),
        migrations.AddField(
            model_name='ordergoods',
            name='sku',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.GoodsSKU', verbose_name='商品SKU'),
        ),
    ]

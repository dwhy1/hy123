from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.db import transaction
from django.conf import settings
from django.contrib.auth.decorators import login_required
import time
from user.models import Address
from goods.models import GoodsSKU
from order.models import OrderInfo, OrderGoods

from TTSX import settings

from datetime import datetime

# from alipay import AliPay


# import os


# 提交订单页面
def OrderPlace(request):
    if request.method == "GET":
        pass
    elif request.method == "POST":
        user = request.user
        sku_ids = request.POST.getlist('sku_ids')
        if not sku_ids:
            # 跳转到购物车页面
            return redirect(reverse('cart:cartInfo'))
        conn = settings.REDIS_CONN
        cart_key = 'cart_%d' % user.id
        skus = []
        total_count = 0
        total_price = 0
        # 遍历sku_ids获取用户要购买的商品信息
        for sku_id in sku_ids:
            # 根据商品的id获取商品的信息
            sku = GoodsSKU.objects.get(id=sku_id)
            # 获取用户索要购买的商品数量
            count = conn.hget(cart_key, sku_id)
            # 计算商品的小计
            amount = sku.price * int(count)
            # 动态给sku只能加属性count，保存购买商品的数量
            sku.count = count
            # 动态给sku增加属性amount，保存购买商品发小计
            sku.amount = amount
            # 追加
            skus.append(sku)
            # 累加计算商品的总件数和总价格
            total_count += int(count)
            total_price += amount
        # 运费：实际开发的时候，属于一个子系统
        transit_price = 10
        # 实付款
        total_pay = total_price + transit_price
        # 获取用户的收件地址
        addrs = Address.objects.filter(user=user)
        # 组织上下文
        sku_ids = ','.join(sku_ids)
        context = {
            'skus': skus,
            'total_count': total_count,
            'total_price': total_price,
            'total_pay': total_pay,
            'transit_price': transit_price,
            'addrs': addrs,
            'sku_ids': sku_ids
        }
        # 使用模板
        return render(request, 'place_order.html', context)


# 订单生成页面
@transaction.atomic
def OrderCommit(requset):
    if requset.method == 'POST':
        user = requset.user
        if not user.is_authenticated():
            # 用户未登录
            return JsonResponse({'res': 0, 'errmsg': '用户未登录'})
        # 接收参数
        addr_id = requset.POST.get('addr_id')
        pay_method = requset.POST.get('pay_method')
        sku_ids = requset.POST.get('sku_ids')

        # 检验参数
        if not all([addr_id, pay_method, sku_ids]):
            return JsonResponse({'res': 1, 'errmsg': '参数不完整'})

        # 校验支付方式
        if pay_method not in OrderInfo.PAY_METHODS.keys():
            return JsonResponse({'res': 2, 'errmsg': '非法的支付方式'})

        # 校验地址
        try:
            addr = Address.objects.get(id=addr_id)
        except Address.DoesNotExist:
            # 地址不存在
            return JsonResponse({'res': 3, 'errmsg': '地址不存在'})

        # todo:创建订单核心业务

        # 组织参数
        # 订单id:20171122181630+用户id
        order_id = datetime.now().strftime('%Y%m%d%H%M%S') + str(user.id)

        # 运费
        transit_price = 10

        # 总数目和总价格
        total_count = 0
        total_price = 0

        # 设置事务保存点
        save_id = transaction.savepoint()
        try:
            # todo:向df_order_info表中添加一条记录
            order = OrderInfo.objects.create(order_id=order_id,
                                             user=user,
                                             addr=addr,
                                             pay_method=pay_method,
                                             total_count=total_count,
                                             total_price=total_price,
                                             transit_price=transit_price)

            # todo:用户的订单中有几个商品，需要向df_order_goods表中加入几条记录
            conn = settings.REDIS_CONN
            cart_key = 'cart_%d' % user.id

            sku_ids = sku_ids.split(',')
            for sku_id in sku_ids:
                for i in range(3):
                    # 获取商品的信息
                    try:
                        # 解决订单并发情况(悲观锁)
                        # select * from df_goods_sku where id=sku_id for update;加锁
                        # sku = GoodsSKU.objects.select_for_update().get(id=sku_id)
                        sku = GoodsSKU.objects.get(id=sku_id)
                    except:
                        # 商品不存在
                        transaction.savepoint_rollback(save_id)  # 回滚到保存点
                        return JsonResponse({'res': 4, 'errmsg': '商品不存在'})

                    # 从redis中获取用户所要购买商品的数量
                    count = conn.hget(cart_key, sku_id)

                    # todo:判断商品的库存
                    if int(count) > sku.stock:
                        transaction.savepoint_rollback(save_id)  # 回滚到保存点
                        return JsonResponse({'res': 6, 'errmsg': '商品库存不足'})

                    # todo:更新商品的库存和销量
                    orgin_stock = sku.stock
                    new_stock = orgin_stock - int(count)
                    new_sales = sku.sales + int(count)

                    # print('user:%d times:%d stock:%d'%(user.id, i, sku.stock))
                    # import time
                    # time.sleep(5)

                    # 解决订单并发情况(乐观锁:冲突较少或者重复操作的代价大的时候使用)
                    # update df_goods_Sku set stock=new_stock, sales=new_sales
                    # where id=sku_id and stock=orgin_Stock
                    # 返回受影响的行数
                    res = GoodsSKU.objects.filter(id=sku_id, stock=orgin_stock).update(stock=new_stock, sales=new_sales)
                    if res == 0:
                        if i == 2:
                            # 尝试的第三次没有成功的话->下单失败
                            transaction.savepoint_rollback(sku_id)
                            return JsonResponse({'res': 7, 'errmsg': '下单失败2'})
                        continue

                    # todo:向df_order_goods表中添加一条记录
                    OrderGoods.objects.create(order=order,
                                              sku=sku,
                                              count=count,
                                              price=sku.price)

                    # todo:累加计算订单商品的总数量和总价格
                    amount = sku.price * int(count)
                    total_count += int(count)
                    total_price += amount

                    # 跳出循环进行后面操作
                    break

            # todo:更新订单信息表中的商品总数量和总价格
            order.total_count = total_count
            order.total_price = total_price
            order.save()
        except Exception as e:
            transaction.savepoint_rollback(save_id)  # 回滚到保存点
            return JsonResponse({'res': 7, 'errmsg': '下单失败'})

        # 提交事务
        transaction.savepoint_commit(save_id)

        # todo:清除用户购物车中对应的记录
        conn.hdel(cart_key, *sku_ids)

        # 返回应答
        return JsonResponse({'res': 5, 'message': '创建成功'})


# 订单字符页面
def OrderPlay(request):
    if request.method == "POST":
        # 用户是否登陆
        user = request.user
        if not user.is_authenticated():
            return JsonResponse({'res': 0, 'errmsg': '用户未登录'})

        # 接收参数
        order_id = request.POST.get('order_id')

        # 校验参数
        if not order_id:
            return JsonResponse({'res': 1, 'errmsg': '无效的订单id'})

        try:
            order = OrderInfo.objects.get(order_id=order_id,
                                          user=user,
                                          pay_method=3,
                                          order_status=1)
        except OrderInfo.DoesNotExist:
            return JsonResponse({'res': 2, 'errmsg': '订单错误'})

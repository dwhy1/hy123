from django.shortcuts import render, redirect, HttpResponse
from shopcart.models import ShopCart
from users.models import Address
from . import models
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.http import require_GET, require_POST, require_safe, require_http_methods
from django.db import transaction


# 订单确认
@require_POST
def order_confirm(request):
    total = 0
    # 得到前端勾选的购物车编号
    shopcart_id_list = request.POST.getlist('buy_goods_id')
    # 购物车对象列表
    shopcart_list = ShopCart.objects.filter(pk__in=shopcart_id_list)
    print(shopcart_list, 3333333333)
    for i in shopcart_list:
        # 购物车商品的数量
        print(i.num, 44444444444444)
        # 更新总价
        total += i.subtotal
    addrs = Address.objects.filter(user=request.user)
    # addr=Address.objects.filter(status=True)
    # print(addr,22222222222)
    # 返回到订单确认页面 购物车对象列表，总计，用户所有地址
    return render(request, 'orders/order_confirm.html',
                  {'shopcart_list': shopcart_list, 'total': total, 'addrs': addrs})


# 支付，生成订单
def order_done(request):
    addr = Address.objects.filter(status=True)[0]
    # 地址字符串拼接
    addr = addr.recv + '--' + addr.phone + '--' + addr.province + '--' + addr.city + '--' + addr.qu + '--' + addr.intro
    shopcart_list_id = request.POST.getlist('sc_id')
    total = request.POST.get('total')
    shopcart_list = ShopCart.objects.filter(pk__in=shopcart_list_id)

    # 事务
    o_id = transaction.savepoint()
    try:
        remark = request.POST['remark'].strip()
        if remark != '':
            # 没有留言
            order = models.Orders(addr=addr, remark=remark, user=request.user, total=total)
            order.save()
            for i in shopcart_list:
                goodsname = i.goods.name
                goodsprice = i.goods.price
                goodsnum = i.num
                goodsimg = i.goods.goodsimg_set.all.last().path
                orderitem = models.OrdersItem(goodsimg=goodsimg, goodsname=goodsname, goodsprice=goodsprice,
                                              goodsnum=goodsnum, order=order, goodssubtotal=i.subtotal)
                orderitem.save()
        else:
            order = models.Orders(addr=addr, user=request.user, total=total)
            order.save()
            for i in shopcart_list:
                goodsname = i.goods.name
                goodsprice = i.goods.price
                goodsnum = i.num
                goodsimg = i.goods.goodsimg_set.last().path
                orderitem = models.OrdersItem(goodsimg=goodsimg, goodsname=goodsname, goodsprice=goodsprice,
                                              goodsnum=goodsnum, order=order, goodssubtotal=i.subtotal)
                orderitem.save()
        # 修改商品销量，库存
        for i in shopcart_list:
            if i.goods.stock >= i.num:
                print(i.num, 777777777777777777777777, '购买数量')
                i.goods.stock -= i.num
                i.goods.count += i.num
                i.goods.save()
            else:
                return render(request, 'shopcart/shopcart_info.html', {'msg': '库存不足'})

        transaction.savepoint_commit(o_id)
        # return render(request,'orders/order_done.html')
        return redirect('orders:order_list')
    except Exception as e:
        print(e)
        transaction.savepoint_rollback(o_id)


# 订单列表
@login_required
def order_list(request):
    # 筛选 所属用户订单状态为1 的订单
    _order_list = models.Orders.objects.filter(user=request.user, status=True).order_by('-time')
    return render(request, 'orders/order_list.html', {'order_list': _order_list})


# 删除订单
@login_required
def del_order(request, o_id):
    # 修改状态为False
    models.Orders.objects.filter(pk=o_id).update(status=False)
    return redirect('orders:order_list')


# 订单详情
@login_required
def order_detail(request, o_id):
    order = models.Orders.objects.filter(pk=o_id)[0]
    orderitems = models.OrdersItem.objects.filter(order=order)
    # orderitems=models.OrdersItem.objects.getlist(order_id=o_id)
    return render(request, 'orders/order_detail.html', {'orderitems': orderitems, 'order': order})

from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.http import require_GET, require_POST
from goods.models import Goods
from . import models
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def add_shopcart(request, g_id, num):
    _goods = Goods.objects.get(pk=g_id)
    # 查询购物车是否有商品
    try:
        shopcart = models.ShopCart.objects.get(user=request.user, goods=_goods)
        shopcart.num += int(num)
        subtotal = _goods.price * shopcart.num
        shopcart.subtotal = subtotal
        shopcart.save()
    except:
        subtotal = _goods.price * int(num)
        shopcart = models.ShopCart(user=request.user, goods=_goods, num=num, subtotal=subtotal)
        shopcart.save()
    return HttpResponse('添加成功')


@login_required
def shopcart_info(request):
    shoplist = models.ShopCart.objects.filter(user=request.user).order_by('-time')
    return render(request, 'shopcart/shopcart_info.html', {'shoplist': shoplist})


@login_required
def del_shopcart(requesrt, p_id):
    shopcart = models.ShopCart.objects.get(pk=p_id)
    shopcart.delete()
    return redirect('shopcart:shopcart_info')


@login_required
def shopcart_update(request, g_id, num):
    print(g_id, num)
    # 购物车id ，和数量
    shopcart = models.ShopCart.objects.get(pk=g_id)
    print(shopcart.goods.price, 2222222222222222222)
    shopcart.num = num
    shopcart.subtotal = int(num) * (shopcart.goods.price)
    shopcart.save()
    return HttpResponse('修改成功')

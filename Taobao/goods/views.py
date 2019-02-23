from django.shortcuts import render

from . import models

from django.http  import HttpResponseRedirect,HttpResponse
from django.core.cache import cache

from shops.models import Store
from users.models import User
import time
#分页
from django.core.paginator import Paginator


# Create your views here.


# 主页
def index(req):
    goods = models.Goods.objects.all()
    goodstype = models.GoodsType.objects.all()
    pagenum = req.GET.get('pagenum', default=1)
    pagin1 = Paginator(goods, 14)
    page = pagin1.page(int(pagenum))
    try:
        user = req.session['loginUser']
        if user.status == str(0):
            mag = {'a': '个人中心', 'b': '/users/news', 'c': '购物车', 'd': '/goods/cart/', 'e': '免费开店', 'f': '/goods/shop/'}
            msg = {'goods': goods, 'goodstype': goodstype, 'mag': mag, 'pagin1':pagin1,'page':page}
            return render(req, 'user/index.html', msg)
        elif user.status == str(1):
            mag = {'a': '个人中心', 'b': "/users/news", 'c': '购物车', 'd': "/goods/cart/", 'e': '我的店铺',
                   'f': '/shops/shop1/'}
            msg = {'goods': goods, 'goodstype': goodstype, 'user': user, 'mag': mag,'pagin1':pagin1,'page':page}
            return render(req, 'user/index.html', msg)
    except Exception as a:
        mag = {'a': '登录', 'b': "/logs/login/", 'c': '免费注册', 'd': "/logs/register/", 'e': '免费开店',
               'f': ''}
        msg = {'goods': goods, 'goodstype': goodstype, 'mag': mag,'pagin1':pagin1,'page':page}

        return render(req, 'user/index.html', msg)

# 开店
def shop(req):
    if req.method == 'GET':
        return render(req, 'user/shop.html')
    elif req.method == 'POST':
        m1 = req.session['loginUser'].username
        print(req.session['loginUser'].id)
        print(m1)
        u1 = req.POST.get('u1')
        if m1 == u1:
            print(111)
            name = req.POST.get('name')
            cover = req.FILES['cover']
            print(cover)
            intro = req.POST.get('intro')
            time1 = time.time()
            print(222)
            Store.objects.create(name = name,cover=cover,intro= intro,opener_time=time1,status =1,users_id=req.session['loginUser'].id)
            req.session['loginUser'].status = 1
            req.session['loginUser'].save()
            return HttpResponseRedirect('/shops/shop1')


# 购物车
def cart(req):
    return render(req,'user/cart.html')


# 商品详情
def good1(req):
    idm = req.GET.get('sid')
    g1 = models.Goods.objects.get(id=idm)
    s1 = g1.goods_store_id
    num = models.Store.objects.get(id=s1)
    return render(req,'user/good1.html', {'num':num, 'g1':g1})


# 买家进店
def shop(req):
    n1 = req.GET.get('sid')
    n2 =models.Store.objects.get(id=n1)
    gt = models.GoodsType.objects.all()
    goods = models.Goods.objects.filter(goods_store_id=n2.id)
    pagenum = req.GET.get('pagenum', default=1)
    pagin1 = Paginator(goods, 14)
    page = pagin1.page(int(pagenum))
    return render(req,'user/store.html', {'n2':n2, 'goodstype':gt, 'page':page})


# 退出
def del1(req):
    del req.session['loginUser']
    return HttpResponseRedirect('/logs/login/')

from django.shortcuts import render,redirect
from goods.models import Goods
from goods.models import GoodsType
from shops.models import Store
import time
#分页
from django.core.paginator import Paginator
from django.http import HttpResponse
# Create your views here.


# 店铺主页
def shop1(req):
    user = req.session['loginUser']
    mu = Store.objects.get(users_id=user.id)
    store = Store.objects.get(users_id=user.id)
    goods = Goods.objects.filter(goods_store_id=mu.id)
    gt = GoodsType.objects.all()
    pagenum = req.GET.get('pagenum', default=1)
    pagin1 = Paginator(goods, 14)
    page = pagin1.page(int(pagenum))
    return render(req, 'user/shp.html', {'goods': goods,'goodstype':gt, 'hh': mu,'store':store,'user':user,'pagin1': pagin1, 'page': page})


# 店铺关店
def off(req):
    user = req.session['loginUser']
    store = Store.objects.get(users_id=user.id)
    print(store.name)
    store.status = 0
    store.save()
    print(store.status)
    print(11)
    return redirect('shops:shop1')


# 店铺开店
def open(req):
    user = req.session['loginUser']
    store = Store.objects.get(users_id=user.id)
    store.status = 1
    store.save()
    return redirect('shops:shop1')


#商品上架
def thing(req):
    if req.method == 'GET':
        return render(req,'user/thing.html')
    elif req.method == 'POST':
        user = req.session['loginUser']
        name = req.POST.get('name')
        price  = req.POST.get('price')
        stock = req.POST.get('stock')
        count= req.POST.get('count')
        desc = req.POST.get('desc')
        img = req.FILES['img']
        tm1 = time.time()
        d1 = user.id
        store = Store.objects.get(users_id=d1)
        Goods.objects.create(name=name,price=price,stock=stock,count=count,desc=desc,img=img, add_time=tm1, goods_detail_type_id = 1,goods_store_id=store.id)
        return redirect('shops:shop1')


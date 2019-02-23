from . import models
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from hashlib import sha1
from goods import models
from django.views.decorators.csrf import csrf_exempt
# 验证码
from . import utils
from io import BytesIO
import time
from django.http import HttpResponseRedirect, HttpResponse
from django.core.cache import cache
import time
# 分页
from django.core.paginator import Paginator


# 登录
def login(req):
    if req.method == 'GET':
        return render(req, 'user/login.html')
    elif req.method == 'POST':
        username = req.POST.get('username')
        password = req.POST.get('userpass')
        yanz = req.POST.get('yanz')
        if yanz == req.session['code']:
            try:
                user = models.User.objects.get(username=username)
                s1 = sha1()
                s1.update(password.encode("utf-8"))
                spwdSha1 = s1.hexdigest()
                if user.userpass == spwdSha1:
                    msg = {'name': '登陆了'}
                    req.session['loginUser'] = user
                    req.session.set_expiry(0)
                    return redirect('goods:index')
                else:
                    msg = {'name': '密码错误'}
                    return render(req, 'user/login.html', msg)
            except Exception as e:
                print(3333)
                msg = {'name': '用户名不存在'}
                return render(req, 'user/login.html', msg)
        else:
            msg = {'name': '验证码错误'}
            return render(req, 'user/login.html', msg)
    return render(req, 'user/login.html')


# 注册页面
def register(req):
    if req.method == 'GET':
        return render(req, 'user/register.html')
    elif req.method == 'POST':
        name = req.POST.get('username')
        age = req.POST.get('age')
        gender = req.POST.get('gender')
        userpass = req.POST.get('userpass')
        phone = req.POST.get('phone')
        nickname = req.POST.get('nickname')
        email = req.POST.get('email')
        yanz = req.POST.get('yanz')
        header = req.FILES['header']
        if yanz == req.session['code']:
            try:
                models.User.usermanager.get(username=name)
                msg = {'name': '用户存在，请重新输入'}
                return render(req, 'user/register.html', msg)
            except Exception as e:
                s1 = sha1()
                s1.update(userpass.encode("utf-8"))
                spwdSha1 = s1.hexdigest()
                time1 = time.time()
                models.User.usermanager.create(username=name, header=header, userpass=spwdSha1, nickname=nickname,
                                               age=age,
                                               gender=gender, phone=phone, email=email, regist_time=time1,
                                               last_login_time=time1, status=0)
                msg = {'name': '注册了,请登录'}
                return render(req, 'user/login.html', msg)
        else:
            msg = {'name': '验证码错误'}
            return render(req, 'user/register.html', msg)


# 验证码
def creataCode(req):
    f = BytesIO()
    img, code = utils.create_code()
    req.session['code'] = code
    img.save(f, 'PNG')
    return HttpResponse(f.getvalue())


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
            mag = {'a': '个人中心', 'b': '/goods/news', 'c': '购物车', 'd': '/goods/shopcart_info/', 'e': '免费开店', 'f': '/goods/debut/'}
            msg = {'goods': goods, 'goodstype': goodstype, 'mag': mag, 'pagin1': pagin1, 'page': page}
            return render(req, 'user/index.html', msg)
        elif user.status == str(1):
            mag = {'a': '个人中心', 'b': "/goods/news", 'c': '购物车', 'd': "/goods/shopcart_info/", 'e': '我的店铺',
                   'f': '/goods/shop1/'}
            msg = {'goods': goods, 'goodstype': goodstype, 'user': user, 'mag': mag, 'pagin1': pagin1, 'page': page}
            return render(req, 'user/index.html', msg)
    except Exception as a:
        mag = {'a': '登录', 'b': "/goods/login/", 'c': '免费注册', 'd': "/goods/register/", 'e': '免费开店',
               'f': ''}
        msg = {'goods': goods, 'goodstype': goodstype, 'mag': mag, 'pagin1': pagin1, 'page': page}

        return render(req, 'user/index.html', msg)


# 开店
def debut(req):
    if req.method == 'GET':
        return render(req, 'user/shop.html')
    elif req.method == 'POST':
        m1 = req.session['loginUser'].username
        print(req.session['loginUser'].id)
        print(m1)
        u1 = req.POST.get('u1')
        if m1 == u1:
            id1 = req.session['loginUser'].id
            name = req.POST.get('name')
            cover = req.FILES['cover']
            intro = req.POST.get('intro')
            time1 = time.time()
            models.Store.objects.create(name=name, cover=cover, intro=intro, opener_time=time1, status=1,
                                        users_id=id1)
            req.session['loginUser'].status = 1
            req.session['loginUser'].save()
            del req.session['loginUser']
            user = models.User.objects.get(id=id1)
            req.session['loginUser'] = user
            return redirect('goods:shop1')


# 购物车
def cart(req):
    if req.method == 'GET':
        return render(req, 'user/cart.html')
    elif req.method == 'POST':
        user = req.session['loginUser']
        n = req.POST.get('count')
        m = req.POST.get('id')
        g1=models.Goods.objects.get(id=m)
        num = int(n)* int(g1.price)
        time1 = time.time()
        models.ShopCart.objects.create(count=n,add_time=time1, subtotal=num,goods_id=m,users_id=user.id)
        return redirect('goods:index')


# 购物车列表
def shopcart_info(req):
    user = req.session['loginUser']
    shoplist = models.ShopCart.objects.filter(users_id=user.id)
    return render(req, 'user/cart.html', {'shoplist': shoplist})

# 删除购物车
def del_shopcart(req):
    p_id = req.GET.get('sid')
    shopcart = models.ShopCart.objects.get(pk=p_id)
    shopcart.delete()
    return redirect('goods:shopcart_info')

# 订单确认
def order_confirm(req):
    user = req.session['loginUser']
    total = 0
    shopcart_id_list = req.POST.getlist('cartCheckBox')
    shopcart_list = models.ShopCart.objects.filter(pk__in=shopcart_id_list)
    for i in shopcart_list:
        total += int(i.subtotal)
    addrs = models.Address.objects.filter(users_id=user.id)
    print(addrs)
    return render(req,'user/demo.html', {'shopcart_list': shopcart_list, 'total': total, 'addrs': addrs})













# 商品详情
def good1(req):
    idm = req.GET.get('sid')
    g1 = models.Goods.objects.get(id=idm)
    s1 = g1.goods_store_id
    num = models.Store.objects.get(id=s1)
    return render(req, 'user/good1.html', {'num': num, 'g1': g1})


# 买家进店
def shop(req):
    n1 = req.GET.get('sid')
    n2 = models.Store.objects.get(id=n1)
    gt = models.GoodsType.objects.all()
    goods = models.Goods.objects.filter(goods_store_id=n2.id)
    pagenum = req.GET.get('pagenum', default=1)
    pagin1 = Paginator(goods, 14)
    page = pagin1.page(int(pagenum))
    return render(req, 'user/store.html', {'n2': n2, 'goodstype': gt, 'page': page})


# 退出主页
def rem(req):
    try:
        del req.session['loginUser']
        return redirect('goods:login')
    except Exception as a:
        return render(req, 'user/login.html')


# 店铺主页
def shop1(req):
    user = req.session['loginUser']
    mu = models.Store.objects.get(users_id=user.id)
    store = models.Store.objects.get(users_id=user.id)
    goods = models.Goods.objects.filter(goods_store_id=mu.id)
    gt = models.GoodsType.objects.all()
    pagenum = req.GET.get('pagenum', default=1)
    pagin1 = Paginator(goods, 14)
    page = pagin1.page(int(pagenum))
    return render(req, 'user/shp.html',{'goods': goods, 'goodstype': gt, 'hh': mu, 'store': store, 'user': user, 'pagin1' : pagin1,'page': page})


# 店铺关店
def off(req):
    user = req.session['loginUser']
    store = models.Store.objects.get(users_id=user.id)
    print(store.name)
    store.status = 0
    store.save()
    print(store.status)
    print(11)
    return redirect('goods:shop1')


# 店铺开店
def open(req):
    user = req.session['loginUser']
    store = models.Store.objects.get(users_id=user.id)
    store.status = 1
    store.save()
    return redirect('goods:shop1')


# 商品上架
def thing(req):
    if req.method == 'GET':
        return render(req, 'user/thing.html')
    elif req.method == 'POST':
        user = req.session['loginUser']
        name = req.POST.get('name')
        price = req.POST.get('price')
        stock = req.POST.get('stock')
        count = req.POST.get('count')
        desc = req.POST.get('desc')
        img = req.FILES['img']
        tm1 = time.time()
        d1 = user.id
        store = models.Store.objects.get(users_id=d1)
        models.Goods.objects.create(name=name, price=price, stock=stock, count=count, desc=desc, img=img, add_time=tm1,goods_detail_type_id=1, goods_store_id=store.id)
        return redirect('goods:shop1')


# 个人信息
def news(req):
    user = req.session['loginUser']
    store = models.Store.objects.get(users_id=user.id)
    try:
        address = models.Address.objects.get(users_id=user.id, status='1')
        return render(req, 'user/person.html', {'user': user, 'store': store, 'address': address})
    except Exception as a:
        print('你瞅啥')
    return render(req, 'user/person.html', {'user': user, 'store': store})


# 修改信息
def alter(req):
    user = req.session['loginUser']
    store = models.Store.objects.get(users_id=user.id)
    if req.method == 'GET':
        return render(req, 'user/alter.html', {'user': user, 'store': store})
    elif req.method == 'POST':
        nickname = req.POST.get('nickname')
        age = req.POST.get('age')
        gender = req.POST.get('gender')
        phone = req.POST.get('phone')
        email = req.POST.get('email')
        header = req.FILES['header']
        user.nickname = nickname
        user.age = age
        user.gender = gender
        user.phone = phone
        user.email = email
        user.header = header
        user.save()
        req.session['loginUser'] = user
        return redirect('goods:news')


# 个人地址
def address(req):
    user = req.session['loginUser']
    address = models.Address.objects.filter(users_id=user.id)
    return render(req, 'user/address.html', {'address': address})


# 添加地址
def add(req):
    if req.method == 'GET':
        return render(req, 'user/add.html')
    elif req.method == 'POST':
        user = req.session['loginUser']
        recv_name = req.POST.get('recv_name')
        recv_phone = req.POST.get('recv_phone')
        provice = req.POST.get('provice')
        city = req.POST.get('city')
        country = req.POST.get('country')
        street = req.POST.get('street')
        desc = req.POST.get('desc')
        models.Address.objects.create(recv_name=recv_name, recv_phone=recv_phone, provice=provice, city=city,
                                      country=country, street=street, desc=desc, status=0, users_id=user.id)
        return redirect('goods:address')


# 删除地址
def del1(req):
    idm = req.GET.get('sid')
    d1 = models.Address.objects.get(id=idm)
    d1.delete()
    return redirect('goods:address')


# 默认地址
def defo1(req):
    user = req.session['loginUser']
    id1 = req.GET.get('sid')
    try:
        s1 = models.Address.objects.get(status='1', users_id=user.id)
        s1.status = 0
        s1.save()
        d2 = models.Address.objects.get(id=id1)
        d2.status = 1
        d2.save()
    except Exception as e:
        print('一剑霜寒十四州')
        d2 = models.Address.objects.get(id=id1)
        d2.status = 1
        d2.save()
    return redirect('goods:address')

from django.shortcuts import render, redirect, reverse, HttpResponse
from . import models
from goods.models import GoodsType
from django.http import JsonResponse
from django.core.serializers import serialize
from django.core.cache import cache
from . import utils
from django.contrib.auth.decorators import login_required


# 类型增加
@login_required
def add_type(request):
    if request.method == 'GET':
        return render(request, 'goods/add_type.html', {'msg': '请仔细填写信息：'})
    elif request.method == 'POST':
        id1 = request.POST['id1'].strip()
        gt_name = request.POST['gt_name'].strip()
        gt_desc = request.POST['gt_desc'].strip()
        gt_parent = request.POST['parent_id'].strip()

        if gt_name == '':
            return render(request, 'goods/add_type.html', {'msg': '类型名字为空'})
        try:
            parent = models.GoodsType.objects.get(pk=gt_parent)
            add_goods_type = models.GoodsType(id=id1, gt_name=gt_name, gt_desc=gt_desc, gt_parent=parent)
            add_goods_type.save()
            return render(request, 'goods/add_type.html', {'msg': '商品类型添加成功'})
        except:
            add_goods_type = models.GoodsType(id=id1, gt_name=gt_name, gt_desc=gt_desc)
            add_goods_type.save()
            return render(request, 'goods/add_type.html', {'msg': '商品类型添加成功'})


# 添加商品
@login_required
def add_goods(request, s_id):
    type1 = GoodsType.objects.filter(gt_parent__isnull=True)
    if request.method == 'GET':
        return render(request, 'goods/add_goods.html', {'s_id': s_id, 'type1': type1})
    elif request.method == 'POST':
        name = request.POST['name'].strip()
        price = request.POST['price'].strip()
        stock = request.POST['stock'].strip()
        desc = request.POST['desc'].strip()
        status = request.POST['status'].strip()
        type2 = request.POST['type2']

        if name == '':
            return render(request, 'goods/add_goods.html', {'msg': '商品名字为空', 's_id': s_id})
        if price == '':
            return render(request, 'goods/add_goods.html', {'msg': '商品价格为空', 's_id': s_id})
        if desc == '':
            return render(request, 'goods/add_goods.html', {'msg': '商品描述为空', 's_id': s_id})
        if stock == '':
            return render(request, 'goods/add_goods.html', {'msg': '商品库存为空', 's_id': s_id})
        if status == '':
            return render(request, 'goods/add_goods.html', {'msg': '商品状态为空', 's_id': s_id})
        store = models.Store.objects.get(pk=s_id)
        goods_type = models.GoodsType.objects.get(pk=type2)

        try:
            path = request.FILES.getlist('cover')
            if len(path) == 0:
                goods = models.Goods(name=name, desc=desc, stock=stock, price=price, status=status, goods_store=store,
                                     goods_type=goods_type)
                goods.save()
                goodsimg = models.GoodsImg(goods=goods)
                goodsimg.save()
                utils.goods_list_cache(request, s_id, ischange=True)
                return render(request, 'goods/add_goods.html', {'msg': '商品添加成功', 's_id': s_id})
            else:
                goods = models.Goods(name=name, desc=desc, stock=stock, price=price, status=status, goods_store=store,
                                     goods_type=goods_type)
                goods.save()
                # 存储多张图片
                for i in path:
                    path = models.GoodsImg(path=i, goods=goods)
                    path.save()
                    utils.goods_list_cache(request, s_id, ischange=True)
                return render(request, 'goods/add_goods.html', {'msg': '商品添加成功', 's_id': s_id})
        except Exception as e:
            print(e, '商品添加错误')
            return render(request, 'goods/add_goods.html', {'msg': '商品类型添加失败', 's_id': s_id})


# 修改商品信息
@login_required
def update_goods(request, g_id):
    type1 = GoodsType.objects.filter(gt_parent__isnull=True)
    goods = models.Goods.objects.get(pk=g_id)
    if request.method == 'GET':
        return render(request, 'goods/update_goods.html', {'goods': goods, 'type1': type1})
    elif request.method == 'POST':
        name = request.POST['name'].strip()
        price = request.POST['price'].strip()
        stock = request.POST['stock'].strip()
        desc = request.POST['desc'].strip()
        status = request.POST['status'].strip()
        # type2 = request.POST['type2']
        if name == '':
            return render(request, 'goods/update_goods.html', {'msg': '商品名字为空', 'goods': goods})
        if price == '':
            return render(request, 'goods/update_goods.html', {'msg': '商品价格为空', 'goods': goods})
        if desc == '':
            return render(request, 'goods/update_goods.html', {'msg': '商品描述为空', 'goods': goods})
        if stock == '':
            return render(request, 'goods/update_goods.html', {'msg': '商品库存为空', 'goods': goods})
        if status == '':
            return render(request, 'goods/update_goods.html', {'msg': '商品状态为空', 'goods': goods})
        # goods_type = models.GoodsType.objects.get(pk=type2)

        try:
            path = request.FILES.getlist('cover')
            if len(path) == 0:
                print('没有传照片')
                goods.name = name
                goods.price = price
                goods.stock = stock
                goods.status = status
                goods.desc = desc
                goods.save()
                utils.goods_list_cache(request, s_id=goods.goods_store_id, ischange=True)
                return redirect(reverse('goods:goods_list', kwargs={'s_id': goods.goods_store_id}))
            else:
                goods.name = name
                goods.price = price
                goods.stock = stock
                goods.status = status
                goods.desc = desc
                goods.save()
                # 存储多张图片
                for i in path:
                    path = models.GoodsImg(path=i, goods=goods)
                    path.save()
                utils.goods_list_cache(request, s_id=goods.goods_store_id, ischange=True)
                return redirect(reverse('goods:goods_list', kwargs={'s_id': goods.goods_store_id}))
        except Exception as e:
            print(e, '商品修改错误')
            return render(request, 'goods/update_goods.html', {'msg': '商品修改失败', 'goods': goods})


# 展示商品详情
def goods_info(request, g_id):
    goods = models.Goods.objects.get(pk=g_id)
    return render(request, 'goods/goods_info.html', {'goods': goods})


# 商品列表
@login_required
def goods_list(request, s_id):
    goodss = utils.goods_list_cache(request, s_id)
    print(goodss, s_id)
    return render(request, 'goods/goods_list.html', {'goodss': goodss})


# 商品类型2
def select2(request):
    type1 = request.GET['type1']
    type2 = GoodsType.objects.filter(gt_parent_id=type1)

    type2 = serialize('json', type2)
    return HttpResponse(type2)

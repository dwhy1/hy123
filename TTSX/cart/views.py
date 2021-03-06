from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse

from goods.models import GoodsSKU
from django.contrib.auth.decorators import login_required
from TTSX import settings

'''
添加商品到购物车：
1）请求方式，采用ajax post
如果涉及到数据的修改（新增，更新。删除），采用post
如果只涉及到数据的获取，采用GET
2)传递参数：商品id(sku_id) 商品数量(count)
ajax发起的请求都在后台，在浏览器中看不到效果
'''


# 购车车商品添加
def CartAdd(request):
    if request.method == 'GET':
        pass
    elif request.method == "POST":
        '''购物车纪录添加'''
        user = request.user
        if not user.is_authenticated():
            # 用户未登录
            return JsonResponse({'res': 0, 'errmsg': '请先登陆！'})
        # 接收数据
        sku_id = request.POST.get('sku_id')
        count = request.POST.get('count')

        # 数据检验
        if not all([sku_id, count]):
            return JsonResponse({'res': 1, 'errmsg': '数据不完整'})

        # 校验添加的商品数量
        try:
            count = int(count)
        except Exception as e:
            # 数目出错
            return JsonResponse({'res': 2, 'errmsg': '商品数目出错'})

        # 检验商品是否存在
        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist:
            # 商品不存在
            return JsonResponse({'res': 3, 'errmsg': '商品不存在'})

        # 业务处理：添加购物车纪录
        conn = settings.REDIS_CONN
        cart_key = 'cart_%d' % user.id
        # 先尝试获取sku_id的值 -> hget  cart_key 属性
        # 如果sku_id在hash中不存在，hget返回None
        cart_count = conn.hget(cart_key, sku_id)
        if cart_count:
            # 累加购物车中的商品数目
            count += int(cart_count)

        # 校验商品的库存
        if count > sku.stock:
            return JsonResponse({'res': 4, 'errmsg': '商品库存不足'})

        # 设置hash中sku_id对应的值
        # hest->如果sku_id已经存在，那么就是更新数据，如果sku_id不存在，那么的就是添加数据
        conn.hset(cart_key, sku_id, count)

        # 计算用户购物车商品的条目数
        total_count = conn.hlen(cart_key)

        # 返回应答
        return JsonResponse({'res': 5, 'total_count': total_count, 'message': '添加成功'})


# 购物车商品展示
@login_required
def cartInfo(request):
    if request.method == 'GET':
        '''显示'''
        # 获取登陆的用户
        user = request.user
        # 获取用户购物车中商品的信息
        conn = settings.REDIS_CONN
        cart_key = 'cart_%d' % user.id
        # {'商品id'：商品数量}
        cart_dict = conn.hgetall(cart_key)

        skus = []
        # 保存用户购物车中商品的总数目和总价格
        total_count = 0
        total_price = 0
        # 遍历获取商品的信息
        for sku_id, count in cart_dict.items():
            # 根据商品的id获取商品的信息
            sku = GoodsSKU.objects.get(id=sku_id)
            # 计算商品的小计
            amount = sku.price * int(count)
            # 动态给sku对象增加一个属性amount,保存商品的小计
            sku.amount = amount
            # 动态给sku对象增加一个属性amount,保存购物车中对应商品的数量
            sku.count = count
            # 添加
            skus.append(sku)

            # 累加计算商品总数目和总价格
            total_count += int(count)
            total_price += amount

        # 组织上下文
        context = {
            'total_count': total_count,
            'total_price': total_price,
            'skus': skus
        }
        return render(request, 'cart.html', context)


# 购物车商品修改
@login_required
def update(request):
    if request.method == "POST":
        user = request.user
        if not user.is_authenticated():
            # 用户未登录
            return JsonResponse({'res': 0, 'errmsg': '请先登陆！'})
        # 接收数据
        sku_id = request.POST.get('sku_id')
        count = request.POST.get('count')
        # 数据检验
        if not all([sku_id, count]):
            return JsonResponse({'res': 1, 'errmsg': '数据不完整'})
        # 校验添加的商品数量
        try:
            count = int(count)
        except Exception as e:
            # 数目出错
            return JsonResponse({'res': 2, 'errmsg': '商品数目出错'})

        # 检验商品是否存在
        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist:
            # 商品不存在
            return JsonResponse({'res': 3, 'errmsg': '商品不存在'})

        # 业务处理：更新购物车纪录
        conn = settings.REDIS_CONN
        cart_key = 'cart_%d' % user.id

        # 校验商品的库存
        if count > sku.stock:
            return JsonResponse({'res': 4, 'errmsg': '商品库存不足'})

        # 更新
        conn.hset(cart_key, sku_id, count)
        total_count = 0
        vals = conn.hvals(cart_key)
        for val in vals:
            total_count += int(val)
        return JsonResponse({'res': 5, 'total_count': total_count, 'message': '更新成功！'})


# 购物车商品删除
@login_required
def delete(request):
    if request.method == "POST":
        user = request.user
        if not user.is_authenticated():
            # 用户未登录
            return JsonResponse({'res': 0, 'errmsg': '请先登陆！'})
        # 接收参数
        sku_id = request.POST.get('sku_id')

        # 数据的校验
        if not sku_id:
            return JsonResponse({'res': 1, 'errmsg': '无效的商品id'})
        # 校验商品是否存在
        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist:
            # 商品不存在
            return JsonResponse({'res': 2, 'errmsg': '商品不存在'})
        # 业务处理：删除购物车纪录
        conn = settings.REDIS_CONN
        cart_key = 'cart_%d' % user.id

        # 删除 hdel
        conn.hdel(cart_key, sku_id)

        # 计算用户购物车中商品总件数{‘1’：5，’2‘:3}
        total_count = 0
        vals = conn.hvals(cart_key)
        for val in vals:
            total_count += int(val)
        # 返回应答
        return JsonResponse({'res': 3, 'total_count': total_count, 'errmsg': '删除成功'})

from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User
from goods.models import Goods, GoodsType
from goods.models import GoodsSKU, IndexGoodsBanner, IndexPromotionBanner, IndexTypeGoodsBanner, GoodsImage
from django.core.cache import cache
from django.core.paginator import Paginator
from TTSX import settings
from django.contrib.auth.decorators import login_required
from . import utils


# 首页
def index(request):
    context = cache.get('index_page_data')
    if context is None:
        # 缓存中没有数据
        # 获取商品的种类信息
        types = GoodsType.objects.all()
        # 获取首页轮播商品信息
        goods_banners = IndexGoodsBanner.objects.all().order_by('index')
        # 获取首页促销活动信息
        promotion_banners = IndexPromotionBanner.objects.all().order_by('index')
        # 获取首页分类商品展示信息
        for type in types:  # GoodsType
            # 获取type种类首页分类商品的图片展示信息
            image_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=1).order_by('index')
            # 获取type种类首页分类商品的文字展示信息
            title_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=0).order_by('index')
            # 动态给type增加属性，分别保存首页分类商品的图片展示信息和文字展示信息
            type.image_banners = image_banners
            type.title_banners = title_banners
        context = {'types': types,
                   'goods_banners': goods_banners,
                   'promotion_banners': promotion_banners}
        # 设置缓存
        # key  value timeout
        cache.set('index_page_data', context, 3600)
    # 获取用户购物车中商品的数目
    user = request.user
    cart_count = 0
    if user.is_authenticated():
        # 用户已登录
        conn = settings.REDIS_CONN
        cart_key = 'cart_%d' % user.id
        cart_count = conn.hlen(cart_key)

    # 组织模板上下文
    context.update(cart_count=cart_count)
    # 使用模板
    return render(request, 'index.html', context)


# 详情页面
def detail(request, goods_id):
    try:
        sku = GoodsSKU.objects.get(id=goods_id)
    except GoodsSKU.DoesNotExist:
        # 商品不存在
        return redirect(reverse('goods:index'))
        # 获取商品的分类信息
    types = GoodsType.objects.all()
    # 获取商品的评论信息
    # sku_orders = OrderGoods.objects.filter(sku=sku).exclude(comment='')

    # 获取新品信息
    new_skus = GoodsSKU.objects.filter(type=sku.type).order_by('-create_time')[:2]

    # 获取同一个SPU的其他规格商品
    same_spu_skus = GoodsSKU.objects.filter(goods=sku.goods).exclude(id=goods_id)

    # 获取用户购物车中商品的数目
    user = request.user
    cart_count = 0
    if user.is_authenticated():
        # 用户已登录
        conn = settings.REDIS_CONN
        cart_key = 'cart_%d' % user.id
        cart_count = conn.hlen(cart_key)
        conn = settings.REDIS_CONN
        # 添加用户的历史记录
        history_key = 'history_%d' % user.id
        # 移除列表中的goods_id
        conn.lrem(history_key, 0, goods_id)
        # 把goods_id插入到列表的左侧
        conn.lpush(history_key, goods_id)
        # 只保存用户最新浏览的5条信息
        conn.ltrim(history_key, 0, 4)

    # 组织模板上下文
    context = {'sku': sku, 'types': types,
               # 'sku_orders': sku_orders,
               'new_skus': new_skus,
               'same_spu_skus': same_spu_skus,
               'cart_count': cart_count}
    # print(context)
    # 使用模板
    return render(request, 'detail.html', context)


# 商品列表
def list(request, type_id, page):
    # 获取种类信息
    try:
        type = GoodsType.objects.get(id=type_id)
    except GoodsType.DoesNotExist:
        # 种类不存在
        return redirect(reverse('goods:index'))

    # 获取商品的分类信息
    types = GoodsType.objects.all()
    sort = request.GET.get('sort')
    if sort == 'price':
        skus = GoodsSKU.objects.filter(type=type).order_by('price')
    elif sort == 'hot':
        skus = GoodsSKU.objects.filter(type=type).order_by('-sales')
    else:
        sort = 'default'
        skus = GoodsSKU.objects.filter(type=type).order_by('-id')

    # 对数据进行分页
    paginator = Paginator(skus, 5)
    # 获取第page页的内容
    try:
        page = int(page)
    except Exception as e:
        page = 1
    if page > paginator.num_pages:
        page = 1
    # 获取第page页的Page实例对象
    skus_page = paginator.page(page)
    # todo: 进行页码的控制，页面上最多显示5个页码
    # 1.如果页码不足5页，页面显示所有页码
    # 2.如果当前页是前3页，显示1-5页
    # 3.如果当前页是后3页，显示后5页
    # 4.其他情况，显示当前页的前2页，当前页，当前页的后2页
    num_pages = paginator.num_pages
    if num_pages < 5:
        pages = range(1, num_pages + 1)
    elif page <= 3:
        pages = range(1, 6)
    elif num_pages - page <= 2:
        pages = range(num_pages - 4, num_pages + 1)
    else:
        pages = range(page - 2, page + 3)

    # 获取新品信息
    new_skus = GoodsSKU.objects.filter(type=type).order_by('-create_time')[:2]
    # 获取用户购物车中商品的数目
    user = request.user
    cart_count = 0
    if user.is_authenticated():
        # 用户已登录
        conn = settings.REDIS_CONN

        # conn = get_redis_connection('default')
        cart_key = 'cart_%d' % user.id
        cart_count = conn.hlen(cart_key)

    # 组织模板上下文
    context = {'type': type, 'types': types,
               'skus_page': skus_page,
               'new_skus': new_skus,
               'cart_count': cart_count,
               'pages': pages,
               'sort': sort}
    # 使用模板
    return render(request, 'list.html', context)


# 商品列表
@login_required
def goods_list(request, s_id):
    goodss = GoodsSKU.objects.filter(goods_store_id=s_id)
    # goodss = utils.goods_list_cache(request, s_id)
    # print(goodss, s_id)
    return render(request, 'goods_list.html', {'goodss': goodss})


# 商品修改
@login_required
def update_goods(request, g_id):
    goods = GoodsSKU.objects.get(pk=g_id)
    if request.method == 'GET':
        return render(request, 'goods_update.html', {'goods': goods, })
    elif request.method == 'POST':
        name = request.POST['name'].strip()
        price = request.POST['price'].strip()
        stock = request.POST['stock'].strip()
        desc = request.POST['desc'].strip()
        status = request.POST['status'].strip()
        if name == '':
            return render(request, 'goods_update.html', {'msg': '商品名字为空', 'goods': goods})
        if price == '':
            return render(request, 'goods_update.html', {'msg': '商品价格为空', 'goods': goods})
        if desc == '':
            return render(request, 'goods_update.html', {'msg': '商品描述为空', 'goods': goods})
        if stock == '':
            return render(request, 'goods_update.html', {'msg': '商品库存为空', 'goods': goods})
        if status == '':
            return render(request, 'goods_update.html', {'msg': '商品状态为空', 'goods': goods})
        try:
            path = request.FILES.getlist('cover')
            if len(path) == 0:
                goods.name = name
                goods.price = price
                goods.stock = stock
                goods.status = status
                goods.desc = desc
                goods.save()
                return redirect(reverse('goods:goods_list', kwargs={'s_id': goods.goods_store_id}))
            else:
                goods.name = name
                goods.price = price
                goods.stock = stock
                goods.status = status
                goods.desc = desc
                goods.image = path
                goods.save()
                return redirect(reverse('goods:goods_list', kwargs={'s_id': goods.goods_store_id}))
        except Exception as e:
            print(e, '商品修改错误')
            return render(request, 'goods_update.html', {'msg': '商品修改失败', 'goods': goods})

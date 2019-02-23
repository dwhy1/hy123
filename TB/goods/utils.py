from . import models

from django.core.cache import cache


def goods_list_cache(request,s_id,ischange=False):
    goodss = cache.get('goods_list1')
    print('缓存中查找商品列表数据')
    if goodss is None or ischange:
        goodss = models.Goods.objects.filter(goods_store_id=s_id)
        cache.set('goods_list1', goodss, timeout=3600)
        print('缓存中没有数据，从数据库查找保存到缓存中')
    return goodss
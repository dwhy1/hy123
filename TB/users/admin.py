from django.contrib import admin
from .models import UserInfo
from store.models import Store
from goods.models import Goods,GoodsImg,GoodsType
from orders.models import OrdersItem,Orders

#第二种注册方法
@admin.register(UserInfo)
class UserAdmin(admin.ModelAdmin):
    list_display = ['nickname','age','sex','phone']
    list_filter = ['age','sex']
    list_per_page = 3
    # 增加和修改的属性
    fields = ["sex", "nickname"]
    #执行按钮调节
    actions_on_bottom = True
    actions_on_top = False

#第一种
# admin.site.register(UserInfo,UserAdmin)
admin.site.register(Store)
admin.site.register(Goods)
admin.site.register(GoodsImg)
admin.site.register(GoodsType)
admin.site.register(Orders)
admin.site.register(OrdersItem)

# admin.site.register(User)
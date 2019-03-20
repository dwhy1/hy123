from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from user.models import UserInfo, Address
from order.models import OrderInfo, OrderGoods
from goods.models import GoodsSKU
from TTSX import settings

# 分页
from django.core.paginator import Paginator
# 验证码
from . import models
from . import utils
from io import BytesIO
import re


# 用户注册
def register(request):
    if request.method == "GET":
        return render(request, 'register.html')
    elif request.method == "POST":
        username = request.POST['user_name']
        password = request.POST['pwd'].strip()
        confirm = request.POST['cpwd'].strip()
        email = request.POST.get("email")
        code = request.POST['code'].strip()
        if code != request.session['code']:
            return render(request, "register.html", {"error": "验证码错误，请重新输入"})
        if username == '':
            return render(request, 'register.html', {'error': '用户名不能为空！'})
        if len(password) < 6:
            return render(request, 'register.html', {'error': '密码小于6位'})
        if password != confirm:
            return render(request, 'register.html', {'error': '两次密码不一致！'})
        try:
            # 判断用户名是否已注册 get 查找到0或多条都会报错
            User.objects.get(username=username)
            return render(request, 'register.html', {'error': '用户名已存在'})
        except:
            try:
                user = User.objects.create_user(username=username, password=password, email=email)
                user.save()
                userinfo = models.UserInfo(user=user, )
                userinfo.save()
                # 跳转到登录页面
                # return redirect('user:user_login')
                return render(request, "login.html", {"error": "注册成功,请登录!"})
            except Exception as e:
                return render(request, "register.html", {"error": "注册失败!"})


# 用户登录
def user_login(request):
    if request.method == "GET":
        # 判断是否记住用户名
        if "username" in request.COOKIES:
            username = request.COOKIES.get("username")
            checked = "checked"
        else:
            username = ""
            checked = ""
        context = {
            "username": username,
            "checked": checked
        }
        return render(request, 'login.html', context)
    elif request.method == "POST":
        username = request.POST.get("username")
        username = str(username).encode('utf-8')
        print(username)
        password = request.POST.get("pwd")
        if not all([username, password]):
            return render(request, "login.html", {"error": "数据不完整"})
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                # 确定用户激活，记录用户的登陆状态
                login(request, user)
                request.session['loginUser'] = user
                request.session.set_expiry(0)
                # 登陆成功之后跳转到首页
                next_url = request.GET.get("next", reverse("goods:index"))
                # 跳转到next_url
                response = redirect(next_url)
                # 判断是否记住用户名
                remember = request.POST.get("remember")
                if remember == "on":
                    # 记住用户名
                    response.set_cookie("username", username, max_age=7 * 24 * 3600)
                else:
                    response.delete_cookie("username")
                return response
            else:
                # 用户未激活
                return render(request, "login.html", {"error": "账户未激活"})
        else:
            # 用户名或者密码错误
            return render(request, "login.html", {"error": "账户或密码有误"})


# 用户退出
@login_required
def user_logout(request):
    logout(request)
    # 跳转首页
    return redirect(reverse("goods:index"))


# 用户中心-信息页
@login_required
def user_info(request):
    user = request.user
    address = Address.objects.get_default_address(user)
    # 获取用户的历史浏览记录
    conn = settings.REDIS_CONN
    history_key = "history_%d" % user.id
    # 获取用户的最新浏览的5个商品的id
    sku_ids = conn.lrange(history_key, 0, 4)
    # 遍历获取用户的浏览的历史商品信息
    goods_li = []
    for id in sku_ids:
        goods = GoodsSKU.objects.get(id=id)
        goods_li.append(goods)
    context = {"page": user, "address": address, "goods_li": goods_li}
    return render(request, 'user_center_info.html', context)


# 用户中心—信息完善修改
@login_required
def user_add(request):
    if request.method == "GET":
        return render(request, 'user_center_add.html')
    elif request.method == "POST":
        nickname = request.POST['nickname'].strip()
        age = request.POST['age'].strip()
        gender = request.POST['gender'].strip()
        user = request.user
        if nickname == '':
            return render(request, 'user_center_add.html', {'msg': '昵称不能为空'})
        if gender == '':
            return render(request, 'user_center_add.html', {'msg': '年龄不能为空'})
        # 年龄要判断
        if age == '' or int(age) < 0 or int(age) > 120:
            return render(request, 'user_center_add.html', {'msg': '年龄输入有误'})
        try:
            headers = request.FILES['headers']
            print(headers)
            user.userinfo.nickname = nickname
            user.userinfo.age = age
            user.userinfo.gender = gender
            user.userinfo.headers = headers
            user.userinfo.save()
            return render(request, "user_center_info.html", {"msg": "用户信息完善完成"})
        except:
            user.userinfo.nickname = nickname
            user.userinfo.age = age
            user.userinfo.gender = gender
            user.userinfo.save()
            return render(request, "user_center_info.html", {"msg": "用户信息完善完成"})


# 用户中心-密码修改
@login_required
def user_pass(request):
    if request.method == "GET":
        return render(request, 'user_center_pass.html')
    elif request.method == "POST":
        # 新密码
        password = request.POST['password']
        # 旧密码
        oldpwd = request.POST['oldpassword']
        confirmpwd = request.POST['confirmpwd']
        if len(password) > 6:
            return render(request, "user_center_pass.html", {"msg": "用户密码长度不能小于3位"})
        if password.strip() != confirmpwd.strip():
            return render(request, "user_center_pass.html", {"msg": "两次密码不一致"})
        username = request.user.username
        user = authenticate(username=username, password=oldpwd)
        if user:
            if user.is_active:
                user.set_password(password)
                user.save()
                logout(request)
                return render(request, 'login.html')
        else:
            return render(request, 'user_center_pass.html', {"mag": '原始密码错误'})


# 用户中心-订单页
@login_required
def user_order(request, page):
    if request.method == "GET":
        user = request.user
        orders = OrderInfo.objects.filter(user=user).order_by('-create_time')
        for order in orders:
            # 根据order_id查询商品信息
            order_skus = OrderGoods.objects.filter(order_id=order.order_id)

            # 遍历order_skus计算商品的小计
            for order_sku in order_skus:
                # 计算小计
                amount = order_sku.count * order_sku.price
                # 动态给order_sku增加属性amount，保存订单商品的小计
                order_sku.amount = amount

            # 动态给order增加属性，保存订单状态标题
            order.status_name = OrderInfo.ORDER_STATUS[order.order_status]
            # 动态给order增加属性，保存订单商品信息
            order.order_skus = order_skus

        # 分页
        paginator = Paginator(orders, 5)

        # 获取第page页的内容
        try:
            page = int(page)
        except Exception as e:
            page = 1

        if page > paginator.num_pages:
            page = 1

        # 获取第page页的Page实例对象
        order_page = paginator.page(page)
        num_pages = paginator.num_pages
        if num_pages < 5:
            pages = range(1, num_pages + 1)
        elif page <= 3:
            pages = range(1, 6)
        elif num_pages - page <= 2:
            pages = range(num_pages - 4, num_pages + 1)
        else:
            pages = range(page - 2, page + 3)
        # 组织上下文
        context = {
            'order_page': order_page,
            'pages': pages,
            'page': 'order123'
        }
        # 使用模板
        return render(request, "user_center_order.html", context)


# 用户中心-地址页
@login_required
def user_address(request):
    if request.method == "GET":
        user = request.user
        address = Address.objects.get_default_address(user)
        return render(request, "user_center_site.html", {"page": "address", "address": address})
    elif request.method == "POST":
        receiver = request.POST.get("receiver")
        addr = request.POST.get("s_province") + request.POST.get("s_city") + request.POST.get("s_county")
        zip_code = request.POST.get("zip_code")
        intro = request.POST.get('intro')
        phone = request.POST.get("phone")
        # 校验数据
        if not all([receiver, addr, phone, intro]):
            return render(request, "user_center_site.html", {"error": "数据不完整"})
        # 校验手机号
        if not re.match(r"^1[3|4|5|7|8][0-9]{9}$", phone):
            return render(request, "user_center_site.html", {"error": "手机号码格式不正确"})
        # 业务处理：地址添加
        # 获取登录用户对应User对象
        user = request.user
        address = Address.objects.get_default_address(user)
        if address:
            is_default = False
        else:
            is_default = True
        # 添加地址
        Address.objects.create(user=user, receiver=receiver, addr=addr, zip_code=zip_code, phone=phone, intro=intro,
                               is_default=is_default)
        # 返回应答，刷新地址页面
        return redirect(reverse("user:user_address"))


# 用户中心-地址修改
@login_required
def addr_update(request):
    addr_lists = models.Address.objects.filter(user=request.user)
    if request.method == "GET":
        return render(request, 'user_center_update.html', {'addr_list': addr_lists})
    elif request.method == "POST":
        a_id = request.POST['addr_default']
        addr = models.Address.objects.get(pk=a_id)
        print(addr.is_default)
        print(addr.intro)
        # 找到其他的非默认地址，循环设置为False
        other_addr = models.Address.objects.exclude(pk=a_id)
        try:
            addr.is_default = True
            addr.save()
            for i in other_addr:
                i.is_default = False
                i.save()
            # 重定向到修改页面
            return redirect('user:addr_update')
        except Exception as e:
            print(e, '修改默认地址失败')
            return render(request, 'user_center_update.html', {'msg': '修改默认地址失败'})


# 用户中心-地址删除
@login_required
def addr_del(request, addr_id):
    address = models.Address.objects.filter(pk=addr_id)
    address.delete()
    return redirect('user:addr_update')


# 验证码
def creataCode(req):
    # 在内存中开辟空间用以生成临时的图片
    f = BytesIO()
    img, code = utils.create_code()
    req.session['code'] = code
    img.save(f, 'PNG')
    return HttpResponse(f.getvalue())

from django.shortcuts import render, redirect, reverse, HttpResponse
from . import models
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# 检查用户
from django.contrib.auth import authenticate, login, logout
from django.db import transaction

from .utils import create_code
from io import BytesIO
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from goods.models import Goods
from store.models import Store
from utils import utils
from django.core.paginator import Paginator
from goods.models import GoodsType


# 主页
def index(request):
    # 当前页
    pageNow = int(request.GET.get('pageNow', 1))
    # 展示所有商品
    goods = utils.cache_allgoods()
    pagesize = settings.PAGESIZE
    paginator = Paginator(goods, pagesize)
    page = paginator.page(pageNow)
    # 查找一级类型
    goodstype1 = GoodsType.objects.filter(gt_parent__isnull=True)
    # 查找二 级类型
    goodstype2 = GoodsType.objects.filter(gt_parent__isnull=False)

    # 找到店铺状态为营业的店列表
    stores = Store.objects.filter(status=1)
    # 找到营业的店的商品
    goods = Goods.objects.filter(goods_store_id__in=stores)
    return render(request, 'index.html', {'goods': goods, 'page': page})


# 注册函数
def register(request):
    if request.method == 'GET':
        return render(request, 'users/register.html', {'msg': '请输入信息'})
    else:
        username = request.POST['name'].strip()
        password = request.POST['pwd'].strip()
        confirm = request.POST['confirm'].strip()
        code = request.POST['code'].strip()
        if username == '':
            return render(request, 'users/register.html', {'msg': '用户名不能为空！'})
        if len(password) < 6:
            return render(request, 'users/register.html', {'msg': '密码小于6位'})
        if password != confirm:
            return render(request, 'users/register.html', {'msg': '两次密码不一致！'})

        if request.session['code'].upper() != code.upper():
            return render(request, 'users/register.html', {'msg': '验证码错误'})
        try:
            # 判断用户名是否已注册 get 查找到0或多条都会报错
            User.objects.get(username=username)
            return render(request, 'users/register.html', {'msg': '用户名已存在'})
        except:
            try:
                user = User.objects.create_user(username=username, password=password)
                userinfo = models.UserInfo(user=user)
                user.save()
                userinfo.save()
                # 跳转到登录页面
                return redirect('users:logins')
                # return render(request, "users/login.html", {"msg": "注册成功,请登录!"})
            except Exception as e:
                print(e, 2222222222222222222222)
                return render(request, "users/register.html", {"msg": "注册失败!"})


# 登录
def logins(request):
    if request.method == 'GET':
        request.session['num'] = 0
        try:
            next_url = request.GET['next']
        except:
            next_url = '/users/index/'
        print(next_url)
        return render(request, 'users/login.html', {'msg': '请填写登录信息！', 'next_url': next_url})
    elif request.method == 'POST':
        request.session['num'] += 1
        username = request.POST['name'].strip()
        password = request.POST['pwd'].strip()
        next_url = request.POST.get('next', '/users/index/')
        print(next_url, '要跳转的页面链接')
        # 判断验证码
        if request.session['num'] > 2:
            print(request.session['num'], '登录错误次数')
            try:
                code = request.POST['code'].strip()
                if request.session['code'].upper() != code.upper():
                    return render(request, 'users/login.html', {'msg': '验证码错误'})
                else:
                    request.session['num'] = 0
            except:
                return render(request, 'users/login.html', {'msg': '验证码不能为空'})

        # 判断用户
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(next_url)
                # return redirect('/users/index/')
            else:
                return render(request, 'users/login.html', {'error_code': 2, 'msg': '账号被锁定'})
        else:
            return render(request, 'users/login.html', {'msg': '用户名或密码错误'})


# 退出
@login_required
def logouts(request):
    logout(request)
    return redirect('users:index')


# 获取验证码
def get_code(request):
    img, code = create_code()
    f = BytesIO()
    request.session['code'] = code
    img.save(f, 'PNG')
    return HttpResponse(f.getvalue())


# 邮箱注册
def reg_email(request):
    if request.method == "GET":
        return render(request, "users/register.html", {})
    else:
        email = request.POST["email"].strip()
        password = request.POST.get("pwd").strip()
        confirmpwd = request.POST.get("confirm").strip()
        code = request.POST['code'].strip()
    # 数据校验
    if request.session['code'] != code:
        return render(request, "users/register.html", {"msg": "验证码错误！！"})
    if len(email) < 1:
        return render(request, "users/register.html", {"msg": "用户邮箱为空！！"})
    if len(password) < 4:
        return render(request, "users/register.html", {"msg": "长度小于 4 位！！"})
    if password != confirmpwd:
        return render(request, "users/register.html", {"msg": "两次密码不一致！！"})
    try:
        user = User.objects.get(username=email)
        return render(request, "users/register.html", {"msg": "名称已经存在"})
    except:

        user = User.objects.create_user(username=email, password=password, email=email)
        userinfo = models.UserInfo(user=user)
    try:
        user.save()
        userinfo.save()
        try:
            # 保存成功，发送邮件
            m_title = "wqx测试电商账号激活邮件"
            m_msg = "点击激活您的账号"
            # 调用 JWT 来加密和解密需要的数据
            serializer = Serializer(settings.SECRET_KEY, expires_in=3600)
            code = serializer.dumps({"confirm": user.id}).decode("utf-8")
            href = "http://ww.ljh.com/user/active/" + code + "/"
            m_html = '<a href="' + href + '" target="_blank">马上点击激活，一个小时内有效</a>'
            send_mail(m_title, m_msg, settings.EMAIL_FROM, [email], html_message=m_html)
            return render(request, "users/login.html", {"msg": "恭喜您，注册成功，请登录邮箱激活账号！！"})
        except Exception as e:
            print(e, 111111111111111)
            return render(request, "users/login.html", {"msg": "恭喜您，注册成功，邮箱发送失败，请点击重新发送"})
    except Exception as e:
        return render(request, "users/register.html", {"msg": "注册失败，请重新注册，或者联系管理员"})


def active(request, token):
    serializer = Serializer(settings.SECRET_KEY, 3600)
    try:
        info = serializer.loads(token)
        active_id = info["confirm"]
        user = models.User.objects.get(pk=active_id)
        user.is_active = True
        user.save()
        return render(request, "users/login.html", {"msg": "恭喜您，激活账号成功，请登录！！"})
    except Exception as e:
        return HttpResponse("激活失败")


# ajax 检查名字
def checkname(request):
    name = request.GET['name'].strip()
    try:
        user = User.objects.get(username=name)
        return JsonResponse({'msg': '该账号已存在,请更换 ', 'success': False})
    except:
        return JsonResponse({'msg': '该账号可用', 'success': True})


# ajax 检查名字
def checkemail(request):
    email = request.GET['email'].strip()
    try:
        user = User.objects.get(username=email)
        return JsonResponse({'msg': '该账号已存在,请更换 ', 'success': False})
    except:
        return JsonResponse({'msg': '该账号可用', 'success': True})


# 展示个人信息
@login_required
def userinfo(request):
    user = request.user
    return render(request, 'users/userinfo.html', {'user': user})


# 修改资料
@login_required
def changeinfo(request):
    user = request.user
    if request.method == 'GET':
        return render(request, 'users/changeinfo.html', {'user': user})

    else:
        nickname = request.POST['nickname'].strip()
        age = request.POST['age'].strip()
        email = request.POST['email'].strip()
        phone = request.POST['phone'].strip()
        sex = request.POST['sex'].strip()

        if nickname == '':
            return render(request, 'users/changeinfo.html', {'msg': '昵称不能为空'})
        # 年龄要判断
        if age == '' or int(age) < 0 or int(age) > 120:
            return render(request, 'users/changeinfo.html', {'msg': '年龄输入有误'})
        if email == '':
            return render(request, 'users/changeinfo.html', {'msg': '邮箱不能为空'})
        if phone == '':
            return render(request, 'users/changeinfo.html', {'msg': '手机号不能为空'})

        try:
            user.userinfo.nickname = nickname
            user.userinfo.age = age
            user.email = email
            user.userinfo.phone = phone
            user.userinfo.sex = sex
            user.save()
            user.userinfo.save()

            # 重定向到个人信息页面
            return redirect('/users/userinfo/')
        except Exception as e:
            print(e)
            return render(request, 'users/changeinfo.html', {'msg': '信息修改失败！！！'})


# 修改头像
@login_required
def changeavatar(request):
    user = request.user
    if request.method == 'GET':
        return render(request, 'users/changeinfo.html', {'user': user})
    else:
        avatar = request.FILES['avatar']
        try:
            user.userinfo.avatar = avatar
            user.userinfo.save()
            return redirect('/users/userinfo/')
        except:
            return render(request, 'users/changeinfo.html', {"msg": '头像修改失败！！'})


# 修改密码
@login_required
def changepwd(request):
    user = request.user
    if request.method == 'GET':
        return render(request, 'users/changeinfo.html', {'user': user})

    else:
        oldpwd = request.POST['oldpwd'].strip()
        newpwd = request.POST['newpwd'].strip()
        confirm = request.POST['confirm'].strip()
        if len(newpwd) < 6:
            return render(request, 'users/changeinfo.html', {'msg': '输入的密码太短'})
        if newpwd != confirm:
            return render(request, 'users/changeinfo.html', {'msg': '输入的密码不一致'})
        if user.check_password(oldpwd):
            pass
        else:
            return render(request, 'users/changeinfo.html', {'msg': '旧密码错误'})
        try:
            user.set_password(newpwd)
            user.save()
            logout(request)
            # 重定向到登录页面
            return redirect('/users/logins/')
        except Exception as e:
            print(e, 22222222222222222222)
            return render(request, 'users/changeinfo.html', {"msg": '密码修改失败！！'})


# 添加地址
def add_addr(request):
    if request.method == 'GET':
        return render(request, 'users/add_addr.html')
    elif request.method == 'POST':
        recv = request.POST['recv'].strip()
        phone = request.POST['phone'].strip()
        province = request.POST['province'].strip()
        city = request.POST['city'].strip()
        qu = request.POST['qu'].strip()
        diqu = request.POST['diqu'].strip()
        intro = request.POST['intro'].strip()
        if recv == '':
            return render(request, 'users/add_addr.html', {'msg': '收件人为空'})
        if phone == '':
            return render(request, 'users/add_addr.html', {'msg': '手机号为空'})
        if intro == '' or province == '' or city == '' or diqu == '' or qu == '':
            return render(request, 'users/add_addr.html', {'msg': '收件人地址不完整'})

    try:
        status = request.POST['status'].strip()
        # 将其他地址改为非默认地址
        addres = models.Address.objects.filter(user=request.user)
        for i in addres:
            i.status = False
            i.save()
        addr = models.Address(diqu=diqu, recv=recv, phone=phone, province=province, city=city, qu=qu, intro=intro,
                              user=request.user, status=True)

    except:
        addr = models.Address(diqu=diqu, qu=qu, recv=recv, phone=phone, province=province, city=city, intro=intro,
                              user=request.user, status=False)
    addr.save()

    return redirect('/users/addr_update/')


# 修改地址
@login_required
def addr_update(request):
    addr_lists = models.Address.objects.filter(user=request.user)
    if request.method == 'GET':
        return render(request, 'users/addr_update.html', {'addr_list': addr_lists})

    elif request.method == 'POST':
        a_id = request.POST['addr_default']
        addr = models.Address.objects.get(pk=a_id)
        # 找到其他的非默认地址，循环设置为False
        other_addr = models.Address.objects.exclude(pk=a_id)
        try:
            addr.status = True
            addr.save()
            for i in other_addr:
                i.status = False
                i.save()
            # 重定向到修改页面
            return redirect('users:addr_update')
        except Exception as e:
            print(e, '修改默认地址失败')
            return render(request, 'users/addr_update.html', {'msg': '修改默认地址失败'})


# 删除地址
@login_required
def addr_del(request, addr_id):
    address = models.Address.objects.filter(pk=addr_id)
    address.delete()
    return redirect('users:addr_update')

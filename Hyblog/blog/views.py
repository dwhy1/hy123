from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from . import models


def index(request):
    return render(request, 'user/index.html')


# 用户登录
def user_login(request):
    if request.method == "GET":
        return render(request, 'user/login.html')
    elif request.method == "POST":
        username = request.POST['username'].strip()
        password = request.POST['password'].strip()

        # 验证验证码
        # code = request.POST['code'].strip()

        user = authenticate(password=password, username=username)

        if user is not None:
            if user.is_active:
                # 验证通过的用户信息保存在request中
                login(request, user)
                # return
                return render(request, "user/login.html", {"msg": "您的账号已被锁定，请联系管理员"})

        else:
            return render(request, "user/login.html", {"msg": "用户名或密码错误。请重新登录"})


# 用户登出
@login_required
def user_logout(request):
    logout(request)
    return render(request, "user/login.html", {'msg': "退出成功,请重新登录"})


# 用户注册
def register(request):
    if request.method == "GET":
        return render(request, 'user/register.html')
    elif request.method == "POST":
        username = request.POST['username'].strip()
        password = request.POST['password']
        confirmpwd = request.POST['confirmpwd']
        age = request.POST['age']
        gender = request.POST['gender']
        # 数据校验

        if username == "":
            return render(request, "user/register.html", {"msg": "用户名称不能为空"})
        if len(password) > 6:
            return render(request, "user/register.html", {"msg": "用户密码长度不能小于3位"})
        if password.strip() != confirmpwd.strio():
            return render(request, "user/register.html", {"msg": "两次密码不一致"})
        if age == "":
            return render(request, "user/register.html", {"msg": "用户年龄不能为空"})
        if gender == "":
            return render(request, "user/register.html", {"msg": "用户性别不能为空"})
        try:
            User.objects.get(username=username)
            return render(request, "user/register.html", {"msg": "用户名已存在，请重新输入"})
        except:
            try:
                user = User.objects.create_user(username=username, password=password)
                userInfo = models.Users(age=age, gender=gender)
                user.save()
                userInfo.save()
                return render(request, "user/login.html", {"msg": "用户注册成功，请登录"})
            except:
                return render(request, "user/register.html", {"msg": "注册失败，请重新注册"})


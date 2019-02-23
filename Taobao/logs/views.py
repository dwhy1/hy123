
# Create your views here.
from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse
from django.http  import HttpResponseRedirect
from hashlib import sha1
# from users import models
from users.models import User
from goods import models
from django.views.decorators.csrf import csrf_exempt
# 验证码
from . import utils
from io import BytesIO
import time


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
                user = User.usermanager.get(username=username)
                s1 = sha1()
                s1.update(password.encode("utf-8"))
                spwdSha1 = s1.hexdigest()
                if user.userpass == spwdSha1:
                    msg = {'name': '登陆了'}
                    req.session['loginUser'] = user
                    req.session.set_expiry(0)
                    return HttpResponseRedirect('/goods/index/')
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
                User.usermanager.get(username=name)
                msg = {'name': '用户存在，请重新输入'}
                return render(req, 'user/register.html', msg)
            except Exception as e:
                s1 = sha1()
                s1.update(userpass.encode("utf-8"))
                spwdSha1 = s1.hexdigest()
                time1 = time.time()
                User.usermanager.create(username=name,header =header,userpass=spwdSha1,nickname=nickname,age=age,gender=gender,phone=phone,email=email,regist_time=time1,last_login_time=time1,status=0)
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
    img.save(f,'PNG')
    return HttpResponse(f.getvalue())









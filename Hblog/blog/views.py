from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse,JsonResponse
from django.contrib.auth.models import User
from comments.models import Comment

# 分页
from django.core.paginator import Paginator
from . import models
from . import utils
from io import BytesIO


# 用户主页
def user_index(request):
    return render(request, 'user/index.html')


# 博客主页
def index(request):
    art_list = models.Article.objects.all().order_by("-starTime")
    pagenum = request.GET.get('pagenum', default=1)
    pagin1 = Paginator(art_list, 4)
    page = pagin1.page(int(pagenum))
    return render(request, 'user/index1.html', {"articles": page, 'pagin1': pagin1})


# 用户登录
def user_login(request):
    if request.method == "GET":
        return render(request, 'user/login.html')
    elif request.method == "POST":
        print(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        # 验证验证码
        code = request.POST['code'].strip()
        if code != request.session['code']:
            return render(request, "user/login.html", {"msg": "验证码错误，请重新输入"})
        user = authenticate(password=password, username=username)
        if user is not None:
            if user.is_active:
                # 验证通过的用户信息保存在request中
                login(request, user)
                request.session['loginUser'] = user
                request.session.set_expiry(0)
                return HttpResponseRedirect('/blog/index/')
            else:
                return render(request, "user/login.html", {"msg": "您的账号已被锁定，请联系管理员"})
        else:
            return render(request, "user/login.html", {"msg": "用户名或密码错误。请重新登录"})


# 用户登出
@login_required
def user_logout(request):
    logout(request)
    return render(request, "user/login.html", {'msg': "退出成功,请重新登录"})


# 验证码
def creataCode(req):
    # 在内存中开辟空间用以生成临时的图片
    f = BytesIO()
    img, code = utils.create_code()
    req.session['code'] = code
    img.save(f, 'PNG')
    return HttpResponse(f.getvalue())


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
        nickname = request.POST['nickname']
        code = request.POST['code'].strip()
        # 数据校验
        if code != request.session['code']:
            return render(request, "user/register.html", {"msg": "验证码错误，请重新输入"})
        if username == "":
            return render(request, "user/register.html", {"msg": "用户名称不能为空"})
        if len(password) > 6:
            return render(request, "user/register.html", {"msg": "用户密码长度不能小于3位"})
        if password.strip() != confirmpwd.strip():
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
                User.objects.get(nickname=nickname)
                return render(request, "user/register.html", {"msg": "用户名已存在，请重新输入"})
            except:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                try:
                    touxiang = request.FILES['touxiang']
                    userInfo = models.Users(age=age, gender=gender, nickname=nickname, headers=touxiang, user=user)
                    userInfo.save()
                    return render(request, "user/login.html", {"msg": "用户注册成功，请登录"})
                except:
                    userInfo = models.Users(age=age, gender=gender, nickname=nickname, user=user, )
                    userInfo.save()
                    return render(request, "user/login.html", {"msg": "用户注册成功，请登录"})


@login_required
# 用户信息
def user_list(request):
    return render(request, "user/user_list.html")


@login_required
# 用户修改
def user_update(request):
    if request.method == "GET":
        id = request.GET['id']
        users = User.objects.get(pk=id)
        return render(request, 'user/user_update.html', {'user': users})
    elif request.method == "POST":
        id = request.POST['id']
        age = request.POST['age']
        gender = request.POST['gender']
        nickname = request.POST['nickname']
        user = User.objects.get(pk=id)
        if age == "":
            return render(request, "user/register.html", {"msg": "用户年龄不能为空"})
        if gender == "":
            return render(request, "user/register.html", {"msg": "用户性别不能为空"})
        try:
            header = request.FILES['header']
            user.users.nickname = nickname
            user.users.age = age
            user.users.gender = gender
            user.users.headers = header
            user.users.save()
            return redirect("/blog/user_list/")
        except:
            user.users.nickname = nickname
            user.users.age = age
            user.users.gender = gender
            user.users.save()
            return redirect("/blog/user_list/")


# 修改密码
@login_required
def user_pass(request):
    if request.method == "GET":
        return render(request, 'user/user_pass.html')
    elif request.method == "POST":
        # 新密码
        password = request.POST['password']
        # 旧密码
        oldpwd = request.POST['oldpassword']
        confirmpwd = request.POST['confirmpwd']
        if len(password) > 6:
            return render(request, "user/user_pass.html", {"msg": "用户密码长度不能小于3位"})
        if password.strip() != confirmpwd.strip():
            return render(request, "user/user_pass.html", {"msg": "两次密码不一致"})
        username = request.user.username
        user = authenticate(username=username, password=oldpwd)
        if user:
            if user.is_active:
                user.set_password(password)
                user.save()
                logout(request)
                return render(request, 'user/login.html')
        else:
            return render(request, 'user/user_pass.html', {"mag": '原始密码错误'})


@login_required
# 博客列表
def article_list(request):
    id = request.user.id
    art_list = models.Article.objects.filter(author_id=id).order_by("-starTime")
    pagenum = request.GET.get('pagenum', default=1)
    pagin1 = Paginator(art_list, 4)
    page = pagin1.page(int(pagenum))
    return render(request, "user/blog.html", {"articles": page, 'pagin1': pagin1})


@login_required
# 添加博客
def article_add(request):
    if request.method == "GET":
        return render(request, "user/blog-single.html")
    elif request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        reamark = content[5:]
        if title == "":
            return render(request, "user/article_add.html", {"msg": "文章标题不能为空"})
        if content == "":
            return render(request, "user/article_add.html", {"msg": "文章内容不能为空"})
        author = request.user
        at = models.Article(title=title, content=content, reamark=reamark, author=author)
        at.save()
        return redirect("blog:article_list")


@login_required
# 修改博客
def article_update(request, a_id):
    if request.method == "GET":
        print("收到修改")
        print(a_id)
        at = models.Article.objects.get(pk=a_id)
        return render(request, "user/detail.html", {"article": at})
    elif request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        reamark = content[5:]
        if title == "":
            return render(request, "user/detail.html", {"msg": "文章标题不能为空"})
        if content == "":
            return render(request, "user/detail.html", {"msg": "文章内容不能为空"})
        at = models.Article.objects.get(pk=a_id)
        at.title = title
        at.content = content
        at.reamark = reamark
        at.save()
        return redirect("blog:article_list")


@login_required
# 删除博客
def article_delete(request, a_id):
    at = models.Article.objects.get(pk=a_id)
    at.delete()
    return redirect("/blog/article_list/")


@login_required
# 个人博客详情
def article_detail(request, a_id):
    at = models.Article.objects.get(pk=a_id)
    return render(request, "user/blogs.html", {"article": at})


@login_required
# 博客详情
def detail(request, a_id):
    article = models.Article.objects.get(pk=a_id)
    # 取出文章评论
    comments = Comment.objects.filter(article=a_id)
    # 'toc': md.toc,
    # 添加comments上下文
    context = {'article': article, 'comments': comments}
    return render(request, "user/blog1.html", context)
#
# def love_add(request, art_id):
#     """点赞设置"""
#     if request.is_ajax():
#         art = models.Article.objects.filter(id=int(art_id))[0]
#         art.love_name += 1
#         art.save()
#         result = {'a': 'ok'}
#         return JsonResponse(result)

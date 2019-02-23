from django.shortcuts import render,redirect
from . import models
from shops.models import Store
from django.http import HttpResponse

# Create your views here.


# 个人信息
def news(req):
    user = req.session['loginUser']
    store =Store.objects.get(users_id=user.id)
    try:
        address=models.Address.objects.get(users_id=user.id,status='1')
        return render(req, 'user/person.html', {'user': user, 'store': store, 'address': address})
    except Exception as a:
        print('你瞅啥')
    return render(req, 'user/person.html', {'user': user, 'store': store})

# 修改信息
def alter(req):
    user = req.session['loginUser']
    store = Store.objects.get(users_id=user.id)
    if req.method == 'GET':
        return render(req, 'user/alter.html',{'user': user, 'store': store})
    elif req.method == 'POST':
        nickname = req.POST.get('nickname')
        age = req.POST.get('age')
        gender = req.POST.get('gender')
        phone = req.POST.get('phone')
        email = req.POST.get('email')
        header = req.FILES['header']
        user.nickname = nickname
        user.age = age
        user.gender = gender
        user.phone = phone
        user.email = email
        user.header = header
        user.save()
        req.session['loginUser'] = user
        return redirect('users:news')

#个人地址
def address(req):
    user = req.session['loginUser']
    address = models.Address.objects.filter(users_id=user.id)
    return render(req,'user/address.html', {'address':address})

# 添加地址
def add(req):
    if req.method =='GET':
        return render(req,'user/add.html')
    elif req.method == 'POST':
        user = req.session['loginUser']
        recv_name = req.POST.get('recv_name')
        recv_phone = req.POST.get('recv_phone')
        provice =req.POST.get('provice')
        city = req.POST.get('city')
        country = req.POST.get('country')
        street = req.POST.get('street')
        desc = req.POST.get('desc')
        models.Address.objects.create(recv_name=recv_name,recv_phone=recv_phone,provice=provice,city=city,country=country,street=street,desc=desc,status=0,users_id=user.id)
        return redirect('users:address')

# 删除地址
def del1(req):
    idm = req.GET.get('sid')
    d1= models.Address.objects.get(id=idm)
    d1.delete()
    return redirect('users:address')

# 默认地址
def defo1(req):
    user = req.session['loginUser']
    id1 = req.GET.get('sid')
    try:
        s1 = models.Address.objects.get(status='1',users_id=user.id)
        s1.status = 0
        s1.save()
        d2 = models.Address.objects.get(id=id1)
        d2.status = 1
        d2.save()
    except Exception as e:
        print('一剑霜寒十四州')
        d2 = models.Address.objects.get(id=id1)
        d2.status = 1
        d2.save()
    return redirect('users:address')



from django.http import JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Count

from tool.login_decorator import loging_check
from . import models
import datetime
import json


# Create your views here.
@loging_check('GET', 'POST', 'DELETE', 'PUT')
def users_list(request):
    # 请求数据
    if request.method == 'GET':
        # 获取url中的参数 page（第几页） limit（每页几条数据）searchParams（搜索信息）
        page = int(request.GET.get('page'))
        limit = request.GET.get('limit')
        searchParams = request.GET.get('searchParams')
        # 如果有搜索信息则进行查询
        if searchParams:
            searchParamsObj = json.loads(searchParams)
            objects = models.UserInfo.objects.filter(telephone__icontains=searchParamsObj['telephone'],
                                                     username__icontains=searchParamsObj['username'],
                                                     is_active=1).order_by('-id')
        else:
            objects = models.UserInfo.objects.filter(is_active=1).order_by('-id')
        # 获取总共有多少信息
        # count = models.UserInfo.objects.aggregate(mycnt=Count('id'))['mycnt']
        count = len(objects)
        # 将object分为每页limit数据
        p = Paginator(objects, limit)
        # 第page页的数据
        obj = p.page(page).object_list
        d = {}
        ls = []
        for i in obj:
            d['id'] = i.id
            d['username'] = i.username
            d['sex'] = i.sex
            d['telephone'] = i.telephone
            if not i.expiration:
                d['expiration'] = i.expiration
            else:
                if i.expiration < datetime.datetime.now():
                    i.whetherExpiration = '已过期'
                    i.balance = 0
                    i.dayNum = '0'+'天'
                    i.save()
                d['expiration'] = i.expiration.strftime('%Y-%m-%d')
            if i.whetherExpiration == '未过期' and i.is_fixed == '是':
                dayNum = i.expiration - datetime.datetime.now()
                i.dayNum = str(dayNum.days + 1) + '天'
                i.save()
            d['balance'] = i.balance
            d['dayNum'] = i.dayNum
            d['whetherExpiration'] = i.whetherExpiration
            d['wealth'] = i.wealth
            d['is_fixed'] = i.is_fixed
            ls.append(d.copy())
        result = {
            "code": 0,
            "msg": "",
            "count": count,
            "data": ls
        }

        return JsonResponse(result)
    if request.method == 'POST':
        username = request.POST.get('username')
        sex = request.POST.get('sex')
        telephone = request.POST.get('telephone')
        if not username:
            result = {'code': 201, 'error': '请输入姓名'}
            return JsonResponse(result)
        if not sex:
            result = {'code': 202, 'error': '请输入性别'}
            return JsonResponse(result)
        if not telephone:
            result = {'code': 203, 'error': '请输入手机号码'}
            return JsonResponse(result)
        old_telephone = models.UserInfo.objects.filter(telephone=telephone, is_active=1)
        if old_telephone:
            result = {'code': 204, 'error': '该手机号已经被注册'}
            return JsonResponse(result)
        if len(telephone) != 11:
            result = {'code': 206, 'error': '手机号长度有误'}
            return JsonResponse(result)
        try:
            models.UserInfo.objects.create(username=username, sex=sex, telephone=telephone)
        except Exception as e:
            result = {'code': 205, 'error': "未知错误"}
            print(e)
            return JsonResponse(result)
        result = {'code': 0}
        return JsonResponse(result)
    if request.method == 'DELETE':
        json_str = request.body
        if not json_str:
            result = {'code': 306, 'error': '没有提交数据'}
            return JsonResponse(result)
        data = json.loads(json_str)
        id_list = [i.get('id') for i in data]
        if len(id_list) == 0:
            result = {'code': 301, 'error': '请选择要删除的对象'}
            return JsonResponse(result)
        for i in id_list:
            p = models.UserInfo.objects.get(id=i)
            p.is_active = 0
            p.save()
        return JsonResponse({'code': 0})
    if request.method == 'PUT':
        json_str = request.body
        if not json_str:
            result = {'code': 305, 'error': '您没有提交数据'}
            return JsonResponse(result)
        data = json.loads(json_str)
        id = data.get('id')
        username = data.get('username')
        sex = data.get('sex')
        telephone = data.get('telephone')
        if not id:
            result = {'code': 302, 'error': 'id不能为空'}
            return JsonResponse(result)
        if not username:
            result = {'code': 303, 'error': '姓名不能为空'}
            return JsonResponse(result)
        if not telephone:
            result = {'code': 304, 'error': '手机号不能为空'}
            return JsonResponse(result)
        user = models.UserInfo.objects.get(id=id)
        if not user:
            result = {'code': 305, 'error': '没有该用户'}
            return JsonResponse(result)
        user.username = username
        user.sex = sex
        user.telephone = telephone
        user.save()
        return JsonResponse({'code': 0})

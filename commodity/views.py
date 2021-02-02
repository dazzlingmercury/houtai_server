from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import CommodityInfo
from member.models import UserInfo
from .models import UserCommodity
import datetime
from tool.login_decorator import loging_check


# Create your views here.
@loging_check('GET', 'POST', 'DELETE', 'PUT')
def commodity_list(request):
    # CommodityInfo.objects.create(name='乐学周卡', money=89, gaveMoney=2, frequency=7, mode='14天内使用(若固定座位则7天内使用)')
    # 请求数据
    if request.method == 'GET':
        # 获取url中的参数 page（第几页） limit（每页几条数据）searchParams（搜索信息）
        page = int(request.GET.get('page'))
        limit = request.GET.get('limit')
        searchParams = request.GET.get('searchParams')
        # 如果有搜索信息则进行查询
        if searchParams:
            searchParamsObj = json.loads(searchParams)
            objects = CommodityInfo.objects.filter(name__icontains=searchParamsObj['name'], is_active=1)
        else:
            objects = CommodityInfo.objects.filter(is_active=1)
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
            d['name'] = i.name
            d['money'] = i.money
            d['gaveMoney'] = i.gaveMoney
            d['frequency'] = i.frequency
            d['updateTime'] = i.updateTime
            d['addTime'] = i.addTime
            d['mode'] = i.mode
            ls.append(d.copy())
        result = {
            "code": 0,
            "msg": "",
            "count": count,
            "data": ls
        }

        return JsonResponse(result)
    if request.method == 'POST':
        name = request.POST.get('name')
        money = request.POST.get('money')
        gaveMoney = request.POST.get('gaveMoney')
        frequency = request.POST.get('frequency')
        mode = request.POST.get('mode')
        if not name:
            result = {'code': 201, 'error': '请输入卡名称'}
            return JsonResponse(result)
        if not money:
            result = {'code': 202, 'error': '请输入卡金额'}
            return JsonResponse(result)
        if not gaveMoney:
            result = {'code': 203, 'error': '请输入赠送金额'}
            return JsonResponse(result)
        if not frequency:
            result = {'code': 204, 'error': '请输入卡次数'}
            return JsonResponse(result)
        old_name = CommodityInfo.objects.filter(name=name, is_active=1)
        if old_name:
            result = {'code': 205, 'error': '该卡类已经被注册'}
            return JsonResponse(result)
        try:
            CommodityInfo.objects.create(name=name, money=money, gaveMoney=gaveMoney, frequency=frequency, mode=mode)
        except:
            result = {'code': 205, 'error': "未知错误"}
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
            p = CommodityInfo.objects.get(id=i)
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
        money = data.get('money')
        mode = data.get('mode')
        name = data.get('name')
        frequency = data.get('frequency')
        gaveMoney = data.get('gaveMoney')

        if not id:
            result = {'code': 302, 'error': '卡号不能为空'}
            return JsonResponse(result)
        if not name:
            result = {'code': 303, 'error': '卡名称不能为空'}
            return JsonResponse(result)
        if not money:
            result = {'code': 304, 'error': '卡金额不能为空'}
            return JsonResponse(result)
        if not gaveMoney:
            result = {'code': 304, 'error': '赠送金额不能为空'}
            return JsonResponse(result)
        if not frequency:
            result = {'code': 304, 'error': '卡次数不能为空'}
            return JsonResponse(result)
        if not mode:
            result = {'code': 304, 'error': '使用说明不能为空'}
            return JsonResponse(result)
        commodity_id = CommodityInfo.objects.get(id=id)
        if not commodity_id:
            result = {'code': 305, 'error': '没有该对象'}
            return JsonResponse(result)
        commodity_id.money = money
        commodity_id.mode = mode
        commodity_id.name = name
        commodity_id.frequency = frequency
        commodity_id.gaveMoney = gaveMoney
        commodity_id.save()
        return JsonResponse({'code': 0})


# 充值接口
@loging_check('GET', 'POST', 'DELETE', 'PUT')
def recharge(request):
    if request.method == 'POST':
        json_str = request.body
        if not json_str:
            result = {'code': 444, 'error': '没有提交数据'}
            return JsonResponse(result)
        data = json.loads(json_str)
        # 用户id
        user_id = data.get('id')
        # 套餐id
        commodity_id = data.get('commodity').split('---')[0].split(':')[-1]
        # 用户对象
        user = UserInfo.objects.get(id=user_id)
        if not user:
            result = {'code': 444, 'error': '没有该用户'}
            return JsonResponse(result)
        # 商品对象
        commodity = CommodityInfo.objects.get(id=commodity_id)
        if not commodity:
            result = {'code': 444, 'error': '没有该套餐'}
            return JsonResponse(result)
        # 将套餐和用户关联（第一次思路 直接两张多对多关联）
        UserCommodity.objects.create(user=user, commodity=commodity)
        # UserCommodity.objects.create(name=commodity.name, money=commodity.money, gave_money=commodity.gaveMoney, number=commodity.frequency)
        # 设置座位是否固定
        user.is_fixed = '否'
        # 获取用户过期时间
        expiration = user.expiration
        # 获取用户余额
        balance = user.balance
        # 获取用户累计充值
        wealth = user.wealth
        # 获取剩余时间
        dayNum = user.dayNum
        # 获取是否过期
        whetherExpiration = user.whetherExpiration
        # 获取卡次数
        frequency = int(commodity.frequency)
        # 获取卡金额
        money = int(commodity.money)
        # 获取赠送金额
        gaveMoney = int(commodity.gaveMoney)

        if not expiration:
            user.expiration = datetime.datetime.now() + datetime.timedelta(days=frequency * 2)
            user.save()
        # 添加到期时间
        if expiration:
            if user.whetherExpiration == '已过期':
                user.expiration = datetime.datetime.now() + datetime.timedelta(days=frequency * 2)
                user.save()
            elif user.whetherExpiration == '未过期':
                user.expiration = user.expiration + datetime.timedelta(days=frequency * 2)
                user.save()
        if not wealth:
            user.wealth = money
        # 添加累计充值
        if wealth:
            user.wealth = int(wealth) + money
        if not balance:
            user.balance = money + gaveMoney
        # 添加余额
        if balance:
            user.balance = int(balance) + money + gaveMoney
        if not dayNum:
            user.dayNum = str(frequency) + '天'
        if dayNum:
            user.dayNum = str(int(dayNum[:-1]) + frequency) + '天'

        if user.expiration > datetime.datetime.now():
            user.whetherExpiration = '未过期'
        else:
            user.whetherExpiration = '已过期'
        user.save()
        return JsonResponse({'code': 0})
    # 用户固定座位后修改数据
    if request.method == 'PUT':
        json_str = request.body
        if not json_str:
            result = {'code': 444, 'error': '没有提交数据'}
            return (result)
        data = json.loads(json_str)
        user_id = data.get('id')
        user = UserInfo.objects.get(id=user_id)
        # 将其状态设置为是
        user.is_fixed = '是'
        # 将其余额清0
        user.balance = 0
        # 获取用户剩余时间
        dayNum = int(user.dayNum[:-1])
        # 获取到期时间
        expiration = user.expiration
        # 判断当天时间 + 剩余时间 是否 大于 过期时间
        #    大的话将过期时间保持不变，剩余时间设置为过期时间减去当天时间
        #    否侧过期时间设置为当天时间 + 剩余时间 ，剩余时间保持不变
        if datetime.datetime.now() + datetime.timedelta(days=dayNum) > expiration:
            day_num = expiration - datetime.datetime.now()
            user.dayNum = str(day_num.days) + '天'
        else:
            user.expiration = datetime.datetime.now() + datetime.timedelta(days=dayNum)
        user.save()
        return JsonResponse({'code': 0})

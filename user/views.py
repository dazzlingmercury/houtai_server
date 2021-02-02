import json
import time

from django.http import JsonResponse
from django.shortcuts import render
import jwt
from .models import User


# Create your views here.

def login(request):
    if request.method == 'POST':
        json_str = request.body
        if not json_str:
            result = {'code': 444, 'error': '没有提交数据'}
            return JsonResponse(result)
        data = json.loads(json_str)
        username = data.get('username')
        password = data.get('password')
        if not username:
            result = {'code': 444, 'error': '请输入用户名'}
            return JsonResponse(result)
        if not password:
            result = {'code': 444, 'error': '请输入密码'}
            return JsonResponse(result)
        users = User.objects.filter(username=username)
        if not users:
            result = {'code': 444, 'error': '用户名或密码错误'}
            return JsonResponse(result)
        if users[0].password != password:
            result = {'code': 444, 'error': '用户名或密码错误'}
            return JsonResponse(result)
        token = make_token(username)
        return JsonResponse({'code': 0, 'username': username, 'token': token.decode()})
    if request.method == "GET":
        pass


# 生成token
def make_token(username, expire=3600 * 24 * 7):
    key = 'shuixingge'
    now_t = time.time()
    payload = {'username': username, 'exp': int(now_t + expire)}
    return jwt.encode(payload, key, algorithm='HS256')

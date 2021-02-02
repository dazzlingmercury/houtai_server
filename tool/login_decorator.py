import jwt
from django.http import JsonResponse

KEY = 'shuixingge'


def loging_check(*methods):
    def _loging_check(func):
        def wrapper(request, *args, **kwargs):
            token = request.META.get("HTTP_AUTHORIZATION")
            if not methods:
                # 如果没传methods参数，直接返回视图
                return func(request, *args, **kwargs)
            # method 有值
            if request.method not in methods:
                return func(request, *args, **kwargs)
            # token 校验
            if not token or token == 'null':
                result = {'code': 110, 'error': '请登录'}
                return JsonResponse(result)
            # 校验token，pyjwt 注意异常检测
            try:
                res = jwt.decode(token, KEY, algorithms='HS256')
            except Exception as e:
                print('---token error is {}'.format(e))
                result = {'code': 110, 'error': '请登录'}
                return JsonResponse(result)
            return func(request, *args, **kwargs)

        return wrapper

    return _loging_check

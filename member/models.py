from django.db import models


# Create your models here.
class UserInfo(models.Model):
    username = models.CharField(max_length=50, verbose_name='姓名', null=False)
    sex = models.CharField(max_length=1, verbose_name='性别')
    telephone = models.CharField(max_length=11, null=False)
    expiration = models.DateTimeField(verbose_name='到期时间', null=True)
    balance = models.CharField(max_length=20, verbose_name='余额', default='')
    dayNum = models.CharField(max_length=10, verbose_name='剩余时间', default='')
    whetherExpiration = models.CharField(max_length=3, verbose_name='是否到期', default='')
    wealth = models.CharField(max_length=20, verbose_name='累计充值', default='')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_date = models.DateTimeField(auto_now=True, verbose_name='最近修改时间')
    is_fixed = models.CharField(max_length=10, verbose_name='是否固定座位', default='否')
    is_active = models.CharField(max_length=1, verbose_name='是否处于激活状态', null=False, default=1)

    class Meta:
        db_table = 'user_info'

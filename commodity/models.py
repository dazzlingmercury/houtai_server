from django.db import models
from member.models import UserInfo


# Create your models here.
class CommodityInfo(models.Model):
    name = models.CharField(max_length=20, verbose_name='卡名称', null=False)
    money = models.CharField(max_length=6, verbose_name='卡金额', null=False)
    gaveMoney = models.CharField(max_length=6, verbose_name='赠送金额', null=False)
    frequency = models.CharField(max_length=6, verbose_name='卡次数', null=False)
    addTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updateTime = models.DateTimeField(auto_now=True, verbose_name='最近修改时间')
    mode = models.TextField(max_length=150)
    is_active = models.CharField(max_length=1, verbose_name='是否处于激活状态', null=False, default=1)


    class Meta:
        db_table = 'commodity_info'


class UserCommodity(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    commodity = models.ForeignKey(CommodityInfo, on_delete=models.CASCADE)
    addTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updateTime = models.DateTimeField(auto_now=True, verbose_name='最近修改时间')

    class Meta:
        db_table = 'user_commodity'

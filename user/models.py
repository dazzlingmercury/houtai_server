from django.db import models


# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=10, verbose_name='用户名')
    password = models.CharField(max_length=20, verbose_name='密码')
    group = models.CharField(max_length=2, verbose_name='用户组')
    addTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updateTime = models.DateTimeField(auto_now=True, verbose_name='最近修改时间')

    class Meta:
        db_table = 'user'

from django.db import models


# Create your models here.

class Account(models.Model):
    username = models.CharField("用户名", max_length=64, unique=True)
    password = models.CharField("密码", max_length=64)


class UserAuthToken(models.Model):
    """
    用户Token表
    """
    user = models.OneToOneField(to="Account", on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True)


class Time(models.Model):
    quest = models.CharField(max_length=32, unique=True)
    startime = models.CharField(max_length=21)
    endtime = models.CharField(max_length=21)
    status = models.CharField(max_length=21)
    # 配置auto_now_add=True,创建记录的时候会把当前时间添加到数据库。
    createtime = models.DateField(auto_now_add=True)
    total = models.CharField(max_length=21,default='123')
    user = models.ForeignKey(to="Account", on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % self.quest






























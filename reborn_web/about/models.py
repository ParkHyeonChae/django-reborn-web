from django.db import models
from users.choice import RANK_CHOICES


class Organization(models.Model):
    name = models.CharField(max_length=8, verbose_name="이름")
    department = models.CharField(max_length=10, verbose_name='부서')
    rank = models.CharField(choices=RANK_CHOICES, max_length=10, verbose_name='직급')
    registered_date = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')

    def __str__(self):
        return self.name


class Circles(models.Model):
    circles_name = models.CharField(max_length=8, verbose_name="동아리이름")
    introduce = models.TextField(verbose_name='동아리소개')
    registered_date = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')

    def __str__(self):
        return self.circles_name


class Labs(models.Model):
    labs_name = models.CharField(max_length=8, verbose_name="연구실이름")
    location = models.CharField(max_length=8, verbose_name='연구실위치')
    introduce = models.TextField(verbose_name='연구실소개')
    registered_date = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')

    def __str__(self):
        return self.labs_name
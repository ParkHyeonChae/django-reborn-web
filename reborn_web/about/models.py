from django.db import models
from users.choice import RANK_CHOICES, PART_CHOICES


class Organization(models.Model):
    name = models.CharField(max_length=8, verbose_name="이름")
    part = models.CharField(choices=PART_CHOICES, max_length=10, verbose_name='부서')
    rank = models.CharField(choices=RANK_CHOICES, max_length=10, verbose_name='직급')
    registered_date = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')

    def __str__(self):
        return self.name

    class Meta:
        db_table = '학생회조직도'
        verbose_name = '학생회조직도'
        verbose_name_plural = '학생회조직도'


class Circles(models.Model):
    circles_name = models.CharField(max_length=8, verbose_name="동아리이름")
    introduce = models.TextField(verbose_name='동아리소개')
    registered_date = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')

    def __str__(self):
        return self.circles_name

    class Meta:
        db_table = '동아리소개'
        verbose_name = '동아리소개'
        verbose_name_plural = '동아리소개'


class Labs(models.Model):
    labs_name = models.CharField(max_length=8, verbose_name="연구실이름")
    location = models.CharField(max_length=16, verbose_name='연구실위치')
    introduce = models.TextField(verbose_name='연구실소개')
    registered_date = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')

    def __str__(self):
        return self.labs_name

    class Meta:
        db_table = '연구실소개'
        verbose_name = '연구실소개'
        verbose_name_plural = '연구실소개'
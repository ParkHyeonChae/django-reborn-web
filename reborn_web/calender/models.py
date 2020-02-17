from django.db import models
from django.utils import timezone


class Calender(models.Model):
    event_id = models.CharField(max_length=40, primary_key=True, verbose_name='id')
    event_name = models.CharField(max_length=200, verbose_name='일정')
    location = models.CharField(max_length=200, verbose_name='장소')
    start_date = models.CharField(max_length=50, verbose_name='시작일')
    end_date = models.CharField(max_length=50, verbose_name='종료일')
    all_day = models.BooleanField(verbose_name='종일')
    description = models.TextField(default="", verbose_name='설명')
    updated = models.DateTimeField(verbose_name='수정일', default=(timezone.now() +timezone.timedelta(minutes=330)))
    deleted = models.BooleanField(default=False, verbose_name='삭제여부')

    def __str__(self):
        return self.event_name

    class Meta:
        db_table = '학사일정'
        verbose_name = '학사일정'
        verbose_name_plural = '학사일정'
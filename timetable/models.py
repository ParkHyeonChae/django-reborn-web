import os
from django.conf import settings
from django.db import models
from users.choice import TIME_CHOICE, TIME_LENGTH_CHOICE, DAY_CHOICE, SUBJECT_GRADE_CHOICE
from django.utils import timezone
from datetime import datetime, timedelta


class TimeTable(models.Model):
    grade = models.CharField(choices=SUBJECT_GRADE_CHOICE, max_length=10, blank=True, verbose_name='학년')
    subject = models.CharField(max_length=30, verbose_name='시험과목명')
    professor = models.CharField(max_length=15, verbose_name='담당교수명')
    day = models.CharField(choices=DAY_CHOICE, max_length=30, verbose_name='시험요일')
    date = models.DateField(verbose_name='시험날짜', null=True)
    time = models.CharField(choices=TIME_CHOICE, max_length=30, verbose_name='시험시간')
    time_length = models.CharField(choices=TIME_LENGTH_CHOICE, max_length=10, default=1, verbose_name="시험시간길이",)
    location = models.CharField(max_length=20, verbose_name='시험장소')
    created = models.DateTimeField(auto_now_add=True, null=True, verbose_name='작성일')
    updated = models.DateTimeField(null=True, blank=True, verbose_name='수정일')
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='students', verbose_name='수강학생', blank=True)

    def save(self, *args, **kwargs):
        if self.pk:
            old_model = TimeTable.objects.get(pk=self.pk)
            for i in ('grade', 'subject', 'professor', 'day', 'date', 'time', 'time_length', 'location'):
                if getattr(old_model, i, None) != getattr(self, i, None):
                    self.updated = timezone.now()
        else: 
            updated = timezone.now()
        super(TimeTable, self).save(*args, **kwargs)

    def __str__(self):
        return self.subject

    @property
    def show_updated(self):
        if self.updated :
            time = datetime.now(tz=timezone.utc) - self.updated
        else :
            time = datetime.now(tz=timezone.utc) - self.created

        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + '분 전'
        elif time < timedelta(hours=6):
            return str(int(time.seconds / 3600)) + '시간 전'
        else:
            return False

    class Meta:
        db_table = '시험시간표'
        verbose_name = '시험시간표'
        verbose_name_plural = '시험시간표'
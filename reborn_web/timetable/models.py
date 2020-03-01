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
    created = models.DateTimeField(auto_now_add=True, verbose_name='작성일')
    updated = models.DateTimeField(auto_now=True, verbose_name='수정일')

    def __str__(self):
        return self.subject

    @property
    def show_updated(self):
        time = datetime.now(tz=timezone.utc) - self.updated
        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + '분 전'
        elif time < timedelta(hours=6):
            return str(int(time.seconds / 3600)) + '시간 전'
        else:
            return False

    # @property
    # def show_created(self):
    #     time = datetime.now(tz=timezone.utc) - self.created
    #     if time < timedelta(hours=6):
    #         return True
    #     else :
    #         return False

    class Meta:
        db_table = '시험시간표'
        verbose_name = '시험시간표'
        verbose_name_plural = '시험시간표'
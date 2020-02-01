from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta


class Anonymous(models.Model):
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='작성자')
    title = models.CharField(max_length=128, verbose_name='제목')
    content = models.TextField(verbose_name='내용')
    hits = models.PositiveIntegerField(verbose_name='조회수', default=0)
    comments = models.PositiveIntegerField(verbose_name='댓글수', null=True)
    files = models.FileField(upload_to='upload_file/%Y/%m/%d', null=True, blank=True, verbose_name='이미지')
    registered_date = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')

    def __str__(self):
        return self.title

    @property
    def created_string(self):
        time = datetime.now(tz=timezone.utc) - self.registered_date

        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + '분 전'
        elif time < timedelta(days=1):
            return str(int(time.seconds / 3600)) + '시간 전'
        elif time < timedelta(days=7):
            time = datetime.now(tz=timezone.utc).date() - self.registered_date.date()
            return str(time.days) + '일 전'
        else:
            return False

    class Meta:
        db_table = '익명게시판'
        verbose_name = '익명게시판'
        verbose_name_plural = '익명게시판'

    
class AnonymousComment(models.Model):
    post = models.ForeignKey(Anonymous, on_delete=models.CASCADE, verbose_name='게시글')
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='댓글작성자')
    content = models.TextField(verbose_name='댓글내용')
    created = models.DateTimeField(auto_now_add=True, verbose_name='작성일')
    deleted = models.BooleanField(default=False, verbose_name='삭제여부')
    reply = models.IntegerField(verbose_name='답글위치', default=0)

    def __str__(self):
        return self.content

    @property
    def created_string(self):
        time = datetime.now(tz=timezone.utc) - self.created

        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + '분 전'
        elif time < timedelta(days=1):
            return str(int(time.seconds / 3600)) + '시간 전'
        elif time < timedelta(days=7):
            time = datetime.now(tz=timezone.utc).date() - self.created.date()
            return str(time.days) + '일 전'
        else:
            return False 

    class Meta:
        db_table = '익명댓글'
        verbose_name = '익명댓글'
        verbose_name_plural = '익명댓글'
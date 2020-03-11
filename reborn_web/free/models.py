import os
from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta
from users.choice import CATEGORY_CHOICES
from uuid import uuid4
from notice.models import get_file_path


class Free(models.Model):
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='작성자')
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=18, verbose_name='분류', default='자유')
    title = models.CharField(max_length=128, verbose_name='제목')
    content = models.TextField(verbose_name='내용')
    hits = models.PositiveIntegerField(verbose_name='조회수', default=0)
    comments = models.PositiveIntegerField(verbose_name='댓글수', null=True)
    files = models.FileField(upload_to=get_file_path, null=True, blank=True, verbose_name='이미지파일') # summernote MultiValueDict : files
    upload_files = models.FileField(upload_to=get_file_path, null=True, blank=True, verbose_name='파일')
    registered_date = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')
    filename = models.CharField(max_length=64, null=True, verbose_name='첨부파일명')

    def __str__(self):
        return self.title

    # def filename(self):
    #     return os.path.basename(self.upload_files.name)

    def delete(self, *args, **kargs):
        if self.upload_files:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.upload_files.path))
        super(Free, self).delete(*args, **kargs)

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
        db_table = '자유게시판'
        verbose_name = '자유게시판'
        verbose_name_plural = '자유게시판'


class Comment(models.Model):
    post = models.ForeignKey(Free, on_delete=models.CASCADE, verbose_name='게시글')
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='댓글작성자')
    # writer = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE, verbose_name='댓글작성자')
    # writer = models.CharField(max_length=17, null=True, verbose_name='댓글작성자')
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
        db_table = '자유게시판 댓글'
        verbose_name = '자유게시판 댓글'
        verbose_name_plural = '자유게시판 댓글'
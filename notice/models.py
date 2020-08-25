import os
from django.conf import settings
from django.db import models
from uuid import uuid4
from django.utils import timezone
from datetime import datetime

# import hashlib

# def get_file_path(instance, filename):
#     base = 'upload_file/%Y/%m/%d'
#     parts = os.path.splitext(filename)
#     ctx = hashlib.sha256()
#     return base + ctx.hexdigest() + parts[1]

def get_file_path(instance, filename):
    # ymd_path = timezone.now().strftime('%Y/%m/%d')
    ymd_path = datetime.now().strftime('%Y/%m/%d')
    uuid_name = uuid4().hex
    # extension = os.path.splitext(filename)[-1].lower()
    # return '/'.join(['upload_file/', ymd_path, uuid_name + extension,])
    return '/'.join(['upload_file/', ymd_path, uuid_name])

# def get_image_path(get_file_path):
#   return '/'.join(['upload_file/', ymd_path, uuid_name])


class Notice(models.Model):
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='작성자')
    title = models.CharField(max_length=128, verbose_name='제목')
    content = models.TextField(verbose_name='내용')
    hits = models.PositiveIntegerField(verbose_name='조회수', default=0)
    upload_images = models.FileField(upload_to=get_file_path, null=True, blank=True, verbose_name='이미지파일')
    upload_files = models.FileField(upload_to=get_file_path, null=True, blank=True, verbose_name='파일')
    registered_date = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')
    top_fixed = models.BooleanField(verbose_name='상단고정', default=False)
    filename = models.CharField(max_length=64, null=True, verbose_name='첨부파일명')

    def __str__(self):
        return self.title

    # def get_filename(self):
    #     return os.path.basename(self.upload_files.name)

    def delete(self, *args, **kargs):
        if self.upload_files:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.upload_files.path))
        super(Notice, self).delete(*args, **kargs)

    class Meta:
        db_table = '공지사항'
        verbose_name = '공지사항'
        verbose_name_plural = '공지사항'
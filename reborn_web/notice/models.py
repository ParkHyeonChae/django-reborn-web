import os
from django.conf import settings
from django.db import models


class Notice(models.Model):
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='작성자')
    title = models.CharField(max_length=128, verbose_name='제목')
    content = models.TextField(verbose_name='내용')
    hits = models.PositiveIntegerField(verbose_name='조회수', default=0)
    files = models.FileField(upload_to='upload_file/%Y/%m/%d', null=True, blank=True, verbose_name='파일')
    registered_date = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')
    top_fixed = models.BooleanField(verbose_name='상단고정', default=False)

    def __str__(self):
        return self.title

    def filename(self):
        return os.path.basename(self.files.name)

    def delete(self, *args, **kargs):
        if self.files:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.files.path))
        super(Notice, self).delete(*args, **kargs)

    class Meta:
        db_table = '공지사항'
        verbose_name = '공지사항'
        verbose_name_plural = '공지사항'
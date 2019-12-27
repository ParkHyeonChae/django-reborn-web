from django.db import models
from django.contrib.auth.models import AbstractUser

# class User(models.Model):
    
#     userID = models.CharField(max_length=32, verbose_name='id')
#     email = models.EmailField(max_length=128, verbose_name='e-mail')
#     password = models.CharField(max_length=64, verbose_name='password')
#     registered_date = models.DateTimeField(auto_now_add=True, verbose_name='registered_Date')
    
#     def __str__(self):
#         return self.userID

class User(AbstractUser):

    GRADE_CHOICES = (
        ("1", "1학년"),
        ("2", "2힉년"),
        ("3", "3학년"),
        ("4", "4학년"),
        ("졸업", "졸업생"),
    )

    LEVEL_CHOICES = (
        ("1", "1_EveryOne"),
        ("2", "2_Certified Member"),
        ("3", "3_Manager"),
        ("4", "4_Supervisor"),
    )

    user_id = models.CharField(max_length=32, verbose_name="아이디", unique=True)
    password = models.CharField(max_length=64, verbose_name="비밀번호")
    email = models.EmailField(max_length=128, verbose_name="이메일", unique=True)
    hp = models.IntegerField(max_length=18, verbose_name="핸드폰번호", blank=True, unique=True)
    name = models.CharField(max_length=32, verbose_name="이름", unique=True)
    student_id = models.IntegerField(max_length=10, verbose_name="학번", blank=True, unique=True)
    grade = models.CharField(choices=GRADE_CHOICES, max_length=18, verbse_name="학년", blank=True)
    level = models.CharField(choices=LEVEL_CHOICES, max_length=18, verbose_name="등급", default=1)
    registered_date = models.DateTimeField(auto_now_add=True, verbose_name="가입일")
    
    def __str__(self):
        return self.user_id

    class Meta:
        db_table = "회원목록"
        verbose_name = "사용자"
        verbose_name_plural = "사용자"    
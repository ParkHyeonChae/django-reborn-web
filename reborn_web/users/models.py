from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

        
class User(AbstractBaseUser):

    objects = UserManager()

    GRADE_CHOICES = (
        ("1", "1학년"),
        ("2", "2학년"),
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
    hp = models.IntegerField(verbose_name="핸드폰번호", null=True, unique=True)
    name = models.CharField(max_length=32, verbose_name="이름", unique=True)
    student_id = models.IntegerField(verbose_name="학번", null=True, unique=True)
    grade = models.CharField(choices=GRADE_CHOICES, max_length=18, verbose_name="학년", null=True)
    level = models.CharField(choices=LEVEL_CHOICES, max_length=18, verbose_name="등급", default=1)
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='가입일')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['name']
    
    def __str__(self):
        return self.user_id

    class Meta:
        db_table = "회원목록"
        verbose_name = "사용자"
        verbose_name_plural = "사용자"    

class UserManager(BaseUserManager):

    def create_user(self, user_id, username, password):
        if not user_id:
            raise ValueError('ID Required!')

        user = self.model(
            user_id=user_id,
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, username, password):

        user = self.create_user(user_id, username, password)

        user.is_superuser = True
        user.save(using=self._db)
        return user

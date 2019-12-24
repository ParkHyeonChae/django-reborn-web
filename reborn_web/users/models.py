from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    GRADE_CHOICES = (
        ("1", "1학년"),
        ("2", "2힉년"),
        ("3", "3학년"),
        ("4", "4학년"),
    )

    DEPARTMENT_CHOICES = (
        ("COMPUTER_ENGINEERING", "컴퓨터공학부")
        ("OTHERS", "타 과")
    )

    STATE_CHOICES = (
        ("재학", "재학")
        ("휴학", "휴학")
        ("졸업", "졸업")
    )

    LEVEL_CHOICES = (
        ("1", "1_EveryOne",
        ("2", "2_Certified Member"),
        ("3", "3_Manager"),
        ("4", "4_Supervisor"),
    )
)
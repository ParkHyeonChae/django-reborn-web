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

    STATE_CHOICES = (
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

    userID = models.CharField(max_length=32, verbose_name='id', unique=True)
    password = models.CharField(max_length=64, verbose_name='password')
    hp = models.IntegerField(max_length=18, verbose_name='phone')
    email = models.EmailField(max_length=128, verbose_name='e-mail')
    name = models.CharField(max_length=32, verbose_name='name')
    studentID = models.IntegerField(max_length=10, verbose_name='studentID')
    state = models.CharField(choices=STATE_CHOICES, max_length=18)
    level = models.CharField(choices=LEVEL_CHOICES, max_length=18, defalt=1)
    registered_date = models.DateTimeField(auto_now_add=True, verbose_name='registered_Date')
    
    def __str__(self):
        return self.userID
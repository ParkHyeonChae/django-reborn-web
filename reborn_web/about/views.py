from django.shortcuts import render, redirect
from users.decorators import login_message_required, admin_required
from .models import Organization, Circles, Labs

# 학생회 조직도 보기
def organization_view(request):
    pass


# 동아리 소개 보기
def circles_view(request):
    pass


# 연구실 소개 보기
def labs_view(request):
    pass
from django.shortcuts import render, redirect
from users.decorators import login_message_required, admin_required
from .models import Organization, Circles, Labs


# 학생회 조직도 보기
def organization_view(request):
    organization_list = Organization.objects.all()
    context = {
        'organization_list': organization_list,
    }
    return render(request, 'about/organization_list.html', context)


# 동아리 소개 보기
def circles_view(request):
    circles_list = Circles.objects.all()
    context = {
        'circles_list': circles_list,
    }
    return render(request, 'about/circles_list.html', context)


# 연구실 소개 보기
def labs_view(request):
    labs_list = Labs.objects.all()
    context = {
        'labs_list': labs_list,
    }
    return render(request, 'about/labs_list.html', context)
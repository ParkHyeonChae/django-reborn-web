from django.shortcuts import render, redirect
from users.decorators import login_message_required, admin_required
from .models import Organization, Circles, Labs
from .forms import OrganizationAddForm, CirclesEditForm, LabsEditForm
import json
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import messages


# 학생회 조직도 보기
def organization_view(request):
    organization_list = Organization.objects.all().order_by('rank')
    context = {
        'organization_list': organization_list,
    }
    return render(request, 'about/organization_list.html', context)


# 학생회 조직도 편집모드
@login_message_required
@admin_required
def organization_update_view(request):
    organization_list = Organization.objects.all().order_by('rank')
    context = {
        'organization_list': organization_list,
    }
    return render(request, 'about/organization_update.html', context)


# 학생회 조직도 추가 AJAX
@admin_required
def organization_add_view(request):
    form = OrganizationAddForm()
    context = {
        'list': form,
    }
    return render(request, 'about/organization_add_form.html', context)


# 학생회 조직도 삭제 AJAX
@admin_required
def organization_delete_view(request):
    pk = request.POST.get('id')
    organization_list = Organization.objects.filter(pk=pk)
    organization_list.delete()
    context = {
        'response': 'success',
    }    
    return HttpResponse(json.dumps(context, cls=DjangoJSONEncoder), content_type = "application/json")


# 학생회 조직도 저장
@admin_required
def organization_save_view(request):
    if request.method == "POST":
        form = OrganizationAddForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('about:organization_update')


# 동아리 소개 보기
def circles_view(request):
    circles_list = Circles.objects.all()
    context = {
        'circles_list': circles_list,
    }
    return render(request, 'about/circles_list.html', context)


# 동아리 소개 수정
@login_message_required
@admin_required
def circles_update_view(request, pk):
    circles = Circles.objects.get(id=pk)
    if request.method == "POST":
        form = CirclesEditForm(request.POST, instance=circles)
        if form.is_valid():
            form.save()
            messages.success(request, "수정되었습니다.")
        return redirect('/about/circles/')
    else:
        circles = Circles.objects.get(id=pk)
        circles_name = circles.circles_name
        form = CirclesEditForm(instance=circles)
        context = {
            'form': form,
            'circles_name': circles_name,
        }   
        return render(request, "about/circles_update.html", context)


# 연구실 소개 보기
def labs_view(request):
    labs_list = Labs.objects.all()
    context = {
        'labs_list': labs_list,
    }
    return render(request, 'about/labs_list.html', context)


# 연구실 소개 수정
@login_message_required
@admin_required
def labs_update_view(request, pk):
    labs = Labs.objects.get(id=pk)
    if request.method == "POST":
        form = LabsEditForm(request.POST, instance=labs)
        if form.is_valid():
            form.save()
            messages.success(request, "수정되었습니다.")
        return redirect('/about/labs/')
    else:
        labs = Labs.objects.get(id=pk)
        labs_name = labs.labs_name
        form = LabsEditForm(instance=labs)
        context = {
            'form': form,
            'labs_name': labs_name,
        }   
        return render(request, "about/labs_update.html", context)
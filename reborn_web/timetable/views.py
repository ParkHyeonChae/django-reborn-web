from django.shortcuts import render, get_object_or_404, redirect
from users.decorators import login_message_required, admin_required
from .forms import TimeTableUpdateForm
from .models import TimeTable
import json
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, HttpResponseRedirect, Http404


# 시험시간표 List
@login_message_required
def time_table_view(request):
    timetable_list = TimeTable.objects.all()
    context = {
        'timetable_list': timetable_list,
    }
    return render(request, 'timetable/timetable_list.html', context)


# 시험시간표 편집모드
@login_message_required
@admin_required
def timetable_updatelist_view(request):
    timetable_list = TimeTable.objects.all()
    context = {
        'timetable_list': timetable_list,
    }
    return render(request, 'timetable/timetable_update.html', context)
    # timetable_list = TimeTable.objects.all()
    # if request.method == "POST":
    #     timetable_list = TimeTable.objects.filter(subject='생물').first()
    #     form = TimeTableUpdateForm(request.POST, instance=timetable_list)
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request, "저장되었습니다.")
    #         return redirect('/timetable/')
    # else:
    #     timetable_list = TimeTable.objects.filter(subject='생물').first()
    #     print(timetable_list)
    #     form = TimeTableUpdateForm(instance=timetable_list)
    #     context = {
    #         'list': timetable_list,
    #     }
    #     return render(request, 'timetable/timetable_update.html', context)


# def timetable_update_view(request):
#     pk = request.POST.get('id')
    
#     data = get_object_or_404(TimeTable, id=pk)
 
#     context = {
#         'subject': data.subject,
#         'professor': data.professor,
#     }    
#     return HttpResponse(json.dumps(context, cls=DjangoJSONEncoder), content_type = "application/json")

#------------------------------------------------
# @admin_required
# def timetable_edit_view(request, pk):
#     timetable_list = TimeTable.objects.get(id=pk)
#     if request.method == "POST":
#         form = TimeTableUpdateForm(request.POST, instance=timetable_list)
#         if form.is_valid():
#             form.save()
#             return redirect('/timetable/update/')
#     else:
#         form = TimeTableUpdateForm(instance=timetable_list)
#         context = {
#             # 'list': timetable_list,
#             'list': form,
#         }
#         return render(request, 'timetable/timetable_edit.html', context)

# 시험시간표 수정 AJAX
@admin_required
def timetable_edit_view(request):
    pk = request.POST.get('id')
    timetable_list = TimeTable.objects.get(id=pk)
    form = TimeTableUpdateForm(instance=timetable_list)
    request.session['timetable_id'] = pk
    
    return render(request, 'timetable/timetable_edit_form.html', {'list':form,})


# 시험시간표 삭제 AJAX
@admin_required
def timetable_delete_view(request):
    pk = request.POST.get('id')
    timetable_list = get_object_or_404(TimeTable, pk=pk)
    timetable_list.delete()
    context = {
        'response': 'success',
    }    
    return HttpResponse(json.dumps(context, cls=DjangoJSONEncoder), content_type = "application/json")


# 시험시간표 수정, 추가 저장
@admin_required
def timetable_save_view(request):
    if request.method == "POST":
        pk = request.session['timetable_id']
        timetable_list = TimeTable.objects.get(id=pk)
        form = TimeTableUpdateForm(request.POST, instance=timetable_list)
        if form.is_valid():
            form.save()
            return redirect('/timetable/update/')

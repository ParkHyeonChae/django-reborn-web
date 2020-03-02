from django.shortcuts import render, get_object_or_404, redirect
from users.decorators import login_message_required, admin_required
from .forms import TimeTableEditForm, TimeTableAddForm
from .models import TimeTable
import json
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, HttpResponseRedirect, Http404


# 시험시간표 List
@login_message_required
def time_table_view(request):
    timetable_list = TimeTable.objects.all().order_by('date')
    first_grade_count = TimeTable.objects.filter(grade='first').count()
    second_grade_count = TimeTable.objects.filter(grade='second').count()
    third_grade_count = TimeTable.objects.filter(grade='third').count()
    fourth_grade_count = TimeTable.objects.filter(grade='fourth').count()
    my_timetable_list = TimeTable.objects.filter(students=request.user)

    context = {
        'timetable_list': timetable_list,
        'first_grade_count': first_grade_count,
        'second_grade_count': second_grade_count,
        'third_grade_count': third_grade_count,
        'fourth_grade_count': fourth_grade_count,
        'my_timetable_list': my_timetable_list,
    }
    return render(request, 'timetable/timetable_list.html', context)


# 시험시간표 편집모드
@login_message_required
@admin_required
def timetable_updatelist_view(request):
    timetable_list = TimeTable.objects.all().order_by('date')
    context = {
        'timetable_list': timetable_list,
    }
    return render(request, 'timetable/timetable_update.html', context)


# 시험시간표 추가 AJAX
@admin_required
def timetable_add_view(request):
    form = TimeTableAddForm()
    grade = request.POST.get('grade')
    context = {
        'list': form,
    } 
    if grade == 'first' :
        context['grade_context'] = 'first_table'
    elif grade == 'second' : 
        context['grade_context'] = 'second_table'
    elif grade == 'third' : 
        context['grade_context'] = 'third_table'
    elif grade == 'fourth' : 
        context['grade_context'] = 'fourth_table'

    return render(request, 'timetable/timetable_add_form.html', context)


# 시험시간표 수정 AJAX
@admin_required
def timetable_edit_view(request):
    pk = request.POST.get('id')
    timetable_list = TimeTable.objects.get(id=pk)
    form = TimeTableEditForm(instance=timetable_list)
    request.session['timetable_id'] = pk
    
    return render(request, 'timetable/timetable_edit_form.html', {'list':form,})


# 시험시간표 삭제 AJAX
@admin_required
def timetable_delete_view(request):
    pk = request.POST.get('id')
    # timetable_list = get_object_or_404(TimeTable, pk=pk)
    timetable_list = TimeTable.objects.filter(pk=pk)
    timetable_list.delete()
    context = {
        'response': 'success',
    }    
    return HttpResponse(json.dumps(context, cls=DjangoJSONEncoder), content_type = "application/json")


# 시험시간표 수정, 추가 저장
@admin_required
def timetable_save_view(request):
    if request.method == "POST":
        if request.POST.get('grade') == 'first_table' :
            form = TimeTableAddForm(request.POST)
            if form.is_valid():
                data = form.save(commit = False)
                data.grade = 'first'
                data.save()
        elif request.POST.get('grade') == 'second_table' :
            form = TimeTableAddForm(request.POST)
            if form.is_valid():
                data = form.save(commit = False)
                data.grade = 'second'
                data.save()
        elif request.POST.get('grade') == 'third_table' :
            form = TimeTableAddForm(request.POST)
            if form.is_valid():
                data = form.save(commit = False)
                data.grade = 'third'
                data.save()
        elif request.POST.get('grade') == 'fourth_table' :
            form = TimeTableAddForm(request.POST)
            if form.is_valid():
                data = form.save(commit = False)
                data.grade = 'fourth'
                data.save()
        else:
            pk = request.session['timetable_id']
            timetable_list = TimeTable.objects.get(id=pk)
            form = TimeTableEditForm(request.POST, instance=timetable_list)
            if form.is_valid():
                form.save()
        return redirect('/timetable/update/')


# 나의 시험시간표 과목추가/삭제
def timetable_my_view(request):
    if request.method == 'POST':
        reset_list = TimeTable.objects.all()
        for subject_reset in reset_list :
            subject_reset.students.remove(request.user)

        add_list = request.POST.getlist('subject')
        for subject_id in add_list :
            subject_list = TimeTable.objects.get(pk=subject_id)
            subject_list.students.add(request.user)

        return redirect('/timetable/')
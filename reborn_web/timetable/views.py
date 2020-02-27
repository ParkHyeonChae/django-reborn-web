from django.shortcuts import render
from .models import TimeTable

def time_table_view(request):
    # first_timetable_list = TimeTable.objects.filter(grade='first').order_by('-created')
    # second_timetable_list = TimeTable.objects.filter(grade='second').order_by('-created')
    # third_timetable_list = TimeTable.objects.filter(grade='third').order_by('-created')
    # fourth_timetable_list = TimeTable.objects.filter(grade='fourth').order_by('-created')

    timetable_list = TimeTable.objects.all()

    context = {
        # 'first_timetable_list': first_timetable_list,
        # 'second_timetable_list': second_timetable_list,
        # 'third_timetable_list': third_timetable_list,
        # 'fourth_timetable_list': fourth_timetable_list,
        'timetable_list': timetable_list,
    }
    return render(request, 'timetable/timetable_list.html', context)
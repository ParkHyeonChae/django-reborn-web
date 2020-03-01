from django.contrib import admin
from .models import TimeTable


class TimeTableAdmin(admin.ModelAdmin):
    list_display = (
        'subject',
        'grade',
        'professor',
        'time',
        'time_length',
        'date',
        'location',
        'created',
        'updated',
    )

admin.site.register(TimeTable, TimeTableAdmin)
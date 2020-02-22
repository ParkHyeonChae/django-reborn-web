from django.contrib import admin
from .models import Calender


class CalenderAdmin(admin.ModelAdmin):
    list_display = (
        'event_name',
        'location',
        'start_date',
        'end_date',
        'all_day',
    )

admin.site.register(Calender, CalenderAdmin)
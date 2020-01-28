from django.contrib import admin
from .models import Free


class FreeAdmin(admin.ModelAdmin):
    list_display = (
        'title', 
        'writer',
        'hits',
        'registered_date',
        )
    search_fields = ('title', 'content', 'writer__user_id',)

admin.site.register(Free, FreeAdmin)
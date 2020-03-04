from django.contrib import admin
from .models import Organization, Circles, Labs


class OrganizationAdmin(admin.ModelAdmin):
    list_display = (
        'name', 
        'part',
        'rank',
        'registered_date',
    )


class CirclesAdmin(admin.ModelAdmin):
    list_display = (
        'circles_name', 
        'introduce',
        'registered_date',
    )


class LabsAdmin(admin.ModelAdmin):
    list_display = (
        'labs_name', 
        'location', 
        'introduce',
        'registered_date',
    )
        

admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Circles, CirclesAdmin)
admin.site.register(Labs, LabsAdmin)
from django.contrib import admin
from .models import User
from django.contrib.auth.models import Group

class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'name', 'student_id', 'grade', 'level', )

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
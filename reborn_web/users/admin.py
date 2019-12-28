from django.contrib import admin
from .models import User

# class UserAdmin(admin.ModelAdmin):
#     #list_display = ('name', 'state', 'level', )
#     list_display = ('email',)

#admin.site.register(User, UserAdmin)
admin.site.register(User)
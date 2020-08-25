from django.contrib import admin
from .models import Anonymous, AnonymousComment


class AnonymousAdmin(admin.ModelAdmin):
    list_display = (
        'title', 
        'writer',
        'comments',
        'registered_date',
        )
    search_fields = ('title', 'content', 'writer__user_id',)


class AnonymousCommentAdmin(admin.ModelAdmin):
    list_display = (
        'post', 
        'content',
        'writer',
        'created',
        'deleted',
        )
    search_fields = ('post__title', 'content', 'writer__user_id',)


admin.site.register(Anonymous, AnonymousAdmin)
admin.site.register(AnonymousComment, AnonymousCommentAdmin)
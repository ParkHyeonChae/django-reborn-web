from django.conf import settings
from django.urls import path
from . import views


app_name = 'timetable'

urlpatterns = [
    path('', views.time_table_view, name='timetable_list'),
    path('update/', views.timetable_updatelist_view, name='timetable_update'),
    path('add/', views.timetable_add_view, name='timetable_add'),
    path('edit/', views.timetable_edit_view, name='timetable_edit'),
    path('delete/', views.timetable_delete_view, name='timetable_delete'),
    path('save/', views.timetable_save_view, name='timetable_save'),
    path('my/', views.timetable_my_view, name='timetable_my'),
]
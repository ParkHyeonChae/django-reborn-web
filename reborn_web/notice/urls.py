from django.urls import path
from . import views

app_name = 'notice'

urlpatterns = [
    path('', views.NoticeListView.as_view(), name='notice_list'),
    path('write/', views.notice_write_view, name='notice_write'),
    path('<int:pk>/', views.notice_detail_view, name='notice_detail'),
    path('<int:pk>/edit/', views.notice_edit_view, name='notice_edit'),
    path('<int:pk>/delete/', views.notice_delete_view, name='notice_delete'),
]
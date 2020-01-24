from django.urls import path
from . import views

app_name = 'notice'

urlpatterns = [
    path('', views.NoticeListView.as_view(), name='notice_list'),
    # path('<int:pk>/', views.NoticeDetailView.as_view(), name='notice_detail'),
    path('<int:pk>/', views.notice_detail_view, name='notice_detail'),
]
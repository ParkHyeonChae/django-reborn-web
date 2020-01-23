from django.urls import path
from . import views

app_name = 'notice'

urlpatterns = [
    path('', views.NoticeListView.as_view(), name='notice'),
    path('<int:pk>/', views.NoticeDetailView.as_view(), name='notice_detail'),
]
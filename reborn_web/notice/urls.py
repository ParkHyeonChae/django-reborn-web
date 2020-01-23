from django.urls import path
from . import views

app_name = 'notice'

urlpatterns = [
    path('', views.NoticeList.as_view(), name='notice'),
]
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from django.contrib import messages
from django.shortcuts import redirect


app_name = 'notice'

def protected_file(request, path, document_root=None):
    messages.error(request, "접근 불가")
    return redirect('/')

urlpatterns = [
    path('', views.NoticeListView.as_view(), name='notice_list'),
    path('write/', views.notice_write_view, name='notice_write'),
    path('<int:pk>/', views.notice_detail_view, name='notice_detail'),
    path('<int:pk>/edit/', views.notice_edit_view, name='notice_edit'),
    path('<int:pk>/delete/', views.notice_delete_view, name='notice_delete'),
    path('download/<int:pk>', views.notice_download_view, name="notice_download"),
]

urlpatterns += static(settings.MEDIA_URL, protected_file, document_root=settings.MEDIA_ROOT)


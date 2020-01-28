from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'free'

urlpatterns = [
    path('', views.FreeListView.as_view(), name='free_list'),
    path('write/', views.free_write_view, name='free_write'),
    path('<int:pk>/', views.free_detail_view, name='free_detail'),
    path('<int:pk>/edit/', views.free_edit_view, name='free_edit'),
    path('<int:pk>/delete/', views.free_delete_view, name='free_delete'),
    path('download/<int:pk>', views.free_download_view, name="free_download"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
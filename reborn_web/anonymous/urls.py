from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'anonymous'

urlpatterns = [
    path('', views.AnonymousListView.as_view(), name='anonymous_list'),
    path('write/', views.anonymous_write_view, name='anonymous_write'),
    path('<int:pk>/', views.anonymous_detail_view, name='anonymous_detail'),
    path('<int:pk>/edit/', views.anonymous_edit_view, name='anonymous_edit'),
    path('<int:pk>/delete/', views.anonymous_delete_view, name='anonymous_delete'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
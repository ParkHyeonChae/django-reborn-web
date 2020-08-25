from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from django.contrib import messages
from django.shortcuts import redirect
from users.decorators import login_message_required
from django.views.static import serve

app_name = 'anonymous'

@login_message_required
def protected_file(request, path, document_root=None):
    return serve(request, path, document_root)

urlpatterns = [
    path('', views.AnonymousListView.as_view(), name='anonymous_list'),
    path('search/', views.anonymous_search_view, name='anonymous_search'),
    path('write/', views.anonymous_write_view, name='anonymous_write'),

    path('<int:pk>/', views.anonymous_detail_view, name='anonymous_detail'),
    path('<int:pk>/edit/', views.anonymous_edit_view, name='anonymous_edit'),
    path('<int:pk>/delete/', views.anonymous_delete_view, name='anonymous_delete'),

    path('<int:pk>/comment/write/', views.comment_write_view, name='comment_write'),
    path('<int:pk>/comment/delete/', views.comment_delete_view, name='comment_delete'),

    path('like/', views.post_like_view, name='post_like'),
]

urlpatterns += static(settings.MEDIA_URL, protected_file, document_root=settings.MEDIA_ROOT)
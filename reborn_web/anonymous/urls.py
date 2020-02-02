from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'anonymous'

urlpatterns = [
    path('', views.AnonymousListView.as_view(), name='anonymous_list'),
    path('write/', views.anonymous_write_view, name='anonymous_write'),
]
from django.urls import path
from . import views


app_name = 'about'

urlpatterns = [
    path('organization/', views.organization_view, name='organization'),
    path('circles/', views.circles_view, name='circles'),
    path('labs/', views.labs_view, name='labs'),
]
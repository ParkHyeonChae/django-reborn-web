from django.urls import path
from . import views


app_name = 'about'

urlpatterns = [
    path('organization/', views.organization_view, name='organization'),
    path('organization/update/', views.organization_update_view, name='organization_update'),
    path('organization/add/', views.organization_add_view, name='organization_add'),
    path('organization/delete/', views.organization_delete_view, name='organization_delete'),
    path('organization/save/', views.organization_save_view, name='organization_save'),
    path('circles/', views.circles_view, name='circles'),
    path('circles/<int:pk>/', views.circles_update_view, name='circles_update'),
    path('labs/', views.labs_view, name='labs'),
    path('labs/<int:pk>/', views.labs_update_view, name='labs_update'),
]
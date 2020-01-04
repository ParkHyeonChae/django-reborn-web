from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # path('', views.index),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
    #path('register/', views.RegisterView.as_view(), name='register'),
    path('register/', views.register_view, name='register'),
]

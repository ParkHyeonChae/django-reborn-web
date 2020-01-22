from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # path('', views.index),
    # path('login/', views.login_view, name='login'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('recovery/', views.RecoveryView.as_view(), name='recovery'),
    path('recovery/id', views.ajax_find_id_view, name='recovery_id'),
    path('recovery/pw', views.ajax_find_pw_view, name='recovery_pw'),
    path('recovery/auth', views.auth_confirm_view, name='recovery_auth'),
    path('recovery/reset/', views.auth_pw_reset_view, name='recovery_pw_reset'),
    # path('recovery/reset/', views.AuthPwResetView.as_view(), name='recovery_pw_reset'),

    path('registerinfo/', views.register_info_view, name='register_info'),
    # path('register/', views.register_view, name='register'),
    path('register/', views.RegisterView.as_view(), name='register'),
    # path('csregister/', views.cs_register_view, name='csregister'),
    path('csregister/', views.CsRegisterView.as_view(), name='csregister'),
    path('registerauth/', views.register_success, name='register_success'),
    path('activate/<str:uid64>/<str:token>/', views.activate, name='activate'),

    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.profile_update_view, name='profile_update'),
    path('profile/delete/', views.profile_delete_view, name='profile_delete'),
    path('profile/password/', views.password_edit_view, name='password_edit'),
]

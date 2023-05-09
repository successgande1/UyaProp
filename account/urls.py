from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('register/', views.register, name='register-account'),
    path('login/', auth_view.LoginView.as_view(template_name='account/login.html'), name = 'account-login'),
    path('success/', views.registration_success, name='success-account'),
    path('profile/', views.user_profile, name='account-profile'),
    path('update/profile/', views.user_update_profile, name='account-profile-update'),
    path('dashboard/', views.index, name='account-dashboard'),
]

from django.urls import path
from . import views
from django.contrib.auth import views as auth_view
from account.views import MyLoginView

urlpatterns = [
    path('register/', views.register, name='register-account'),
    path('login/', MyLoginView.as_view(), name = 'account-login'),
    path('success/', views.registration_success, name='success-account'),
    path('profile/', views.user_profile, name='account-profile'),
    path('update/profile/', views.user_update_profile, name='account-profile-update'),
    path('dashboard/', views.index, name='account-dashboard'),
]

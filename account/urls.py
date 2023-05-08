from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('register/', views.register, name='register-account'),
    path('', auth_view.LoginView.as_view(template_name='account/login.html'), name = 'account-login'),
    path('success/', views.registration_success, name='success-account'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register-account'),
    path('success/', views.registration_success, name='success-account'),
]

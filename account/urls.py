from django.urls import path

from . import views

urlpatterns = [
    
    path('register/', views.account, name = 'register-account'),
  
]
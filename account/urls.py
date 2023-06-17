from django.urls import path
from . import views
from django.contrib.auth import views as auth_view
from account.views import MyLoginView

urlpatterns = [
    path('register/', views.register, name='register-account'),
    path('login/', MyLoginView.as_view(), name = 'account-login'),
    
    path('profile/', views.user_profile, name='account-profile'),
    path('update/profile/', views.update_profile, name='account-profile-update'),
    path('dashboard/', views.index, name='account-dashboard'), 
    path('landlord/dashboard/', views.landlord_dashboard, name='landlord-dashboard'),
    path('agent/dashboard/', views.agent_dashboard, name='agent-dashboard'),
    path('prospect/dashboard/', views.prospect_dashboard, name='prospect-dashboard'),
    path('default/dashboard/', views.default_dashboard, name='default-dashboard'),
    path('change-password/', views.change_password, name='change_password'),
    path('password-change-done/', views.password_change_done, name='password_change_done'),
    path('logout/', auth_view.LogoutView.as_view(template_name='account/logout.html'), name = 'account-logout'),
]

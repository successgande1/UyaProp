from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from . forms import *
from realestate.models import *
from . models import *

#Register New User Method
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Create a new user object
            user = form.save()
            # Get the user_type value from the form
            user_type = form.cleaned_data['user_type']
            # Create a new object based on the user_type
            if user_type == 'landlord':
                Landlord.objects.create(user=user)
            elif user_type == 'agent':
                Agent.objects.create(user=user)
            elif user_type == 'prospect':
                Prospect.objects.create(user=user)
            # Log the user in and redirect to the homepage
            login(request, user)
            return redirect('success-account')
    else:
        form = RegistrationForm()
    context =  {
        'form': form,
        'page_title': 'Register',
        }
    return render(request, 'account/register.html', context)

class MyLoginView(LoginView):
    template_name = 'login.html'

#Registration Successful method
def registration_success(request):
    if request.user.is_authenticated:
        try:
            user_profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            # If the user does not have a profile, redirect them to the update profile page.
            return redirect('register-account')
        else:
            return redirect('account-dashboard')
        
       
    else:
        # If the user is not authenticated, redirect them to the registration page.
        return redirect('register-account')
    

#User Account Dashboard method
def index(request):
    if request.user.is_authenticated:
        try:
            user_profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            # If the user does not have a profile, redirect them to the update profile page.
            return redirect('register-account')
        
        # Check if the required fields are empty
        if not user_profile.phone_number or not user_profile.address or not user_profile.image:
            # If any of the required fields are empty, redirect the user to the update profile page.
            
            return redirect('account-profile-update')
        else:
            # If all the required fields are filled out, redirect the user to their profile page.
            
            context = {
                'page_title':'Dashboard',
            }
            return render(request, 'account/add_property.html', context)
    else:
        # If the user is not authenticated, redirect them to the registration page.
        return redirect('register-account')
    
#User Profile Method
def user_profile(request):
    context = {
        'page_titel': 'Profile',
    }
    return render(request, 'account/profile_details.html', context)

#View User Profile Method
def user_update_profile(request):
    context = {
        'page_title': 'Update Profile',
    }
    return render(request, 'account/update_profile.html', context)
    
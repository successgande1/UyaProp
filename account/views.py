from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login

from . forms import *
from realestate.models import *

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

def registration_success(request):
    context =  {
        
        'page_title': 'Update Profile',
        }
    return render(request, 'account/update_profile.html', context)
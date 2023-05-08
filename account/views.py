from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .forms import RegistrationForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user_type = form.cleaned_data['user_type']

            user = User.objects.create_user(username=username, password=password)
            user_profile = user.profile
            user_profile.user_type = user_type
            user_profile.save()

            return redirect('success')
    else:
        form = RegistrationForm()
    return render(request, 'account/register.html', {'form': form})

def registration_success(request):
    return render(request, 'account/success.html')

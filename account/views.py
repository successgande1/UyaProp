from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from . forms import *

#Register New User Method
def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST) 
        if form.is_valid():
            form.save()
           
            return redirect('success-account')
    else:
        form = CreateUserForm()
    context = {
        'form':form,
        'page_title':'Register',
    }
    return render(request, 'account/register.html', context)

def registration_success(request):
    return render(request, 'account/update_profile.html')

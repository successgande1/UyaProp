from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import *

# Home Page View.
def index(request):
    context = {
        'page_title':'Ease to Locate Ease to Rent... | UyaProp',   
    }
    return render(request, 'pages/index.html', context)

#About Us View
def about(request):
    context = {
        'page_title':'Easy Accommodation in Nigeria | UyaProp',   
    }
    return render(request, 'pages/about.html', context)

#Our Services Page View
def services(request):
    context = {
        'page_title':'Property Management with Ease in Nigeria | UyaProp',   
    }
    return render(request, 'pages/services.html', context)

#Property View
def property(request):
    context = {
        'page_title':'Free Property Management in Nigeria | UyaProp',   
    }
    return render(request, 'pages/property.html', context)

#Contact Us View
def contact(request):
    context = {
        'page_title':'Contact Us | UyaProp',   
    }
    return render(request, 'pages/contact.html', context)

#Blog View
def blog(request):
    context = {
        'page_title':'Property Management Blog | UyaProp',   
    }
    return render(request, 'pages/blog.html', context)
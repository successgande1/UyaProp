from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import *
from realestate.models import *
from .forms import *
from itertools import chain

# Home Page View.
def index(request):
    form = SearchForm(request.GET or None)
    #Get all the available properties and sort with slice
    listings = Property.objects.filter(is_available=True).order_by('-last_updated')[:6]
    #Get all the Landlords
    landlords = Landlord.objects.all()
    agents = Agent.objects.all()
    #Combine the Landlord and Agent queries
    combined_list = list(chain(landlords, agents))

    if form.is_valid():
        listings = form.search()

    context = {
        'listings': listings,
        'combined_list': combined_list,
        'form': form,
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
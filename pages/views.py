from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import *
from realestate.models import *
from .forms import *
from itertools import chain
from django.core.paginator import Paginator

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
        'page_title':'Ease to Locate Property | UyaProp'
    }
    return render(request, 'pages/index.html', context)



#About Us View
def about(request):
    #Get all the listed properties
    listings = Property.objects.filter(is_available=True).order_by('-last_updated')[:6]
    #Get all the Landlords
    landlords = Landlord.objects.all()
    agents = Agent.objects.all()
    #Combine the Landlord and Agent queries
    combined_list = list(chain(landlords, agents))
    context = {
        'combined_list': combined_list,
        'listings':listings,
        'page_title':'Easy Accommodation in Nigeria | UyaProp',   
    }
    return render(request, 'pages/about.html', context)

#Our Services Page View
def services(request):
    listings = Property.objects.filter(is_available=True).order_by('-last_updated')[:6]
    #Get all the Landlords
    landlords = Landlord.objects.all()
    agents = Agent.objects.all()
    #Combine the Landlord and Agent queries
    combined_list = list(chain(landlords, agents))

    context = {
        'combined_list': combined_list,
        'listings':listings,
        'page_title':'Property Management with Ease in Nigeria | UyaProp',   
    }
    return render(request, 'pages/services.html', context)

#Property View
def property(request):
    #Get all the property listings
    properties = Property.objects.order_by('-last_updated')
    # Paginate Property list
    paginator = Paginator(properties, 4)  # Show 4 properties per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'properties': page_obj,
        'page_title':'Free Property Management in Nigeria | UyaProp',   
        'total_properties': paginator.count,
    }
    return render(request, 'pages/property.html', context)

#Contact Us page View
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            phone = form.cleaned_data['phone']
            content = form.cleaned_data['content']
            Contact.objects.create(name=name, email=email, subject=subject, phone=phone, content=content)
            messages.success(request, 'Message sent successfully.')
            return redirect('pages-contact')
    else:
        form = ContactForm()
    context = {
        'form':form,
        'page_title':'Contact Us | UyaProp',   
    }
    return render(request, 'pages/contact.html', context)

#Blog View
def blog(request):
    context = {
        'page_title':'Property Management Blog | UyaProp',   
    }
    return render(request, 'pages/blog.html', context)
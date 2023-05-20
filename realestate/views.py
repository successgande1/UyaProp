from django.shortcuts import render
from . models import *
# Create your views here.
#Add Property View
def add_property(request):
    context = {
        'page_title': 'Add Property',
    }
    return render(request, 'realestate/add_property.html', context)

#Landlord and agents prospects
def landlord_agents_prospects(request):
    context = {
        'page_title': 'Prospects',
    }
    return render(request, 'realestate/landlord_agent_prospect.html', context)

#Landlord and agents Listing
def property_listing(request):
    context = {
        'page_title': 'Property Listing',
    }
    return render(request, 'realestate/landlord_agent_listing.html', context)

#Listings
def listings(request):
    context = {
        'page_title': 'Listings',
    }
    return render(request, 'realestate/listings.html', context)
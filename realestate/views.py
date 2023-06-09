from django.shortcuts import render, redirect,  get_object_or_404
from . models import *
from . forms import *
from django.contrib.auth import logout
from django.utils.crypto import constant_time_compare
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user
from django.db.models import Q
from django.core.paginator import Paginator
# Create your views here.
#Add Property View

@login_required(login_url='account-login')
def add_property(request):
    # Get user session type
    user_type = request.session.get('user_type')
    if user_type is None:
        logout(request)
        messages.warning(request, 'Session expired. Please log in again.')
        return redirect('account-login')

    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property_instance = form.save(commit=False)

            # Set the appropriate Landlord or Agent based on user login type
            if user_type == 'landlord':
                property_instance.landlord = request.user.landlord
            elif user_type == 'agent':
                property_instance.agent = request.user.agent

            property_instance.save()
            return redirect('property_detail', property_id=property_instance.pk)
    else:  # Move the else statement here
        # Get the properties for the current user
        if user_type == 'landlord':
            properties = Property.objects.filter(landlord__user=request.user).prefetch_related('agent').order_by('-last_updated')[:6]
        elif user_type == 'agent':
            properties = Property.objects.filter(agent__user=request.user).prefetch_related('landlord').order_by('-last_updated')[:6]
        else:
            properties = None

        form = PropertyForm()

    context = {
        'page_title': 'Add Property',
        'form': form,
        'properties': properties,
    }
    return render(request, 'realestate/add_property.html', context)


#Landlord/Agent Property Detail view
@login_required(login_url='account-login')
def property_detail(request, property_id):
    user_type = request.session.get('user_type')
    if user_type is None:
        logout(request)
        messages.warning(request, 'Session expired. Please log in again.')
        return redirect('account-login')  # Replace 'login' with your actual login URL
    
    property_instance = get_object_or_404(Property, pk=property_id)

    properties = []  # Initialize 'properties' as an empty list

    property_owner = None

    # Get the properties for the current user
    if user_type == 'landlord':
        properties = Property.objects.filter(landlord__user=request.user).prefetch_related('agent').order_by('-last_updated')[:4]
        
    elif user_type == 'agent':
        properties = Property.objects.filter(agent__user=request.user).prefetch_related('landlord').order_by('-last_updated')[:4]
        
    elif user_type == 'prospect':
        properties = Property.objects.order_by('-last_updated')[:4]
        if property_instance.landlord:
            property_owner = property_instance.landlord
        elif property_instance.agent:
            property_owner = property_instance.agent
        #Get the Property instances using product key
        property_instance = get_object_or_404(Property, pk=property_id)
        #Get the Prospect details
        prospect = request.user.prospect_profile
        #Construct message for sending for Contacting Landlord or Agent
        message = f"Prospect Full Name: {prospect.user.profile.full_name}\nEmail: {prospect.user.profile.email}\nPhone Number: {prospect.user.profile.phone_number}\nProperty Interested In: {property_instance}"
        #Send Message Notification
        Notification.objects.create(property=property_instance, prospect=prospect, message=message)

        messages.success(request, 'Notification sent successfully with your Contact Details.')
        redirect('listings')
    
    context = {
        'user_type':user_type,
        'properties':properties,
        'property_owner': property_owner,
        'page_title': 'Property Detail',
        'property': property_instance,
    }
    return render(request, 'realestate/landlord_agent_property.html', context)

#Landlord and agents prospects
@login_required
def landlord_agents_prospects(request):
    context = {
        'page_title': 'Prospects',
    }
    return render(request, 'realestate/landlord_agent_prospect.html', context)

#Landlord and agents Listing
@login_required(login_url='account-login')
def landlord_agent_property_listing(request):
    #Get the session user type
    user_type = request.session.get('user_type')
    #Check if user type is NOT in the session and logout the user
    if user_type is None:
        logout(request)
        messages.warning(request, 'Session expired. Please log in again.')
        return redirect('account-login')  
    
    # Get the properties for the current user
    if user_type == 'landlord':
        properties = Property.objects.filter(landlord__user=request.user).prefetch_related('agent')
    elif user_type == 'agent':
        properties = Property.objects.filter(agent__user=request.user).prefetch_related('landlord')

    #Property Search Form
    form = SearchPropertyForm(request.GET)
    if form.is_valid():
        value = form.cleaned_data['value']
        filter_condition = Q(property_type__icontains=value) | Q(address__icontains=value) | Q(state__icontains=value)

        # Apply additional filter based on user type
        if user_type == 'landlord':
            filter_condition &= Q(landlord__user=request.user)
        elif user_type == 'agent':
            filter_condition &= Q(agent__user=request.user)
        #Query Properties and apply filter based on the user filter above
        properties = properties.filter(filter_condition)
        if not properties:
            messages.info(request, 'No properties match your search query.')

     # Paginate the properties
    paginator = Paginator(properties, 6)  # Show 6 properties per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'form': form,
         'properties': page_obj,
        'page_title': f'{user_type} Property Listing',
        'total_properties': paginator.count,
    }
    return render(request, 'realestate/landlord_agent_listing.html', context)

#Edit Property
@login_required(login_url='account-login')
def edit_property(request,property_id):
    user_type = request.session.get('user_type')
    if user_type is None:
        logout(request)
        messages.warning(request, 'Session expired. Please log in again.')
        return redirect('account-login')  
    
    property_instance = get_object_or_404(Property, pk=property_id)

    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property_instance)
        if form.is_valid():
            form.save()
            return redirect('property_detail', property_id=property_instance.pk)
    else:
        # Get the properties for the current user
        if user_type == 'landlord':
            properties = Property.objects.filter(landlord__user=request.user).prefetch_related('agent').order_by('-last_updated')[:6]
        elif user_type == 'agent':
            properties = Property.objects.filter(agent__user=request.user).prefetch_related('landlord').order_by('-last_updated')[:6]
        else:
            properties = None

        form = PropertyForm(instance=property_instance)
    context = {
        'page_title':'Edit Property',
        'form':form,
        'properties':properties,
    }
    return render(request, 'realestate/add_property.html', context)

#Listings
@login_required(login_url='account-login')
def listings(request):
    #Get the session user type
    user_type = request.session.get('user_type')
    #Check if user type is NOT in the session and logout the user
    if not constant_time_compare(user_type, 'prospect'):
        logout(request)
        messages.warning(request, 'Session expired. Please log in again.')
        return redirect('account-login')  
    #Get all listed properties
    properties = Property.objects.order_by('-last_updated')

    # Paginate the properties
    paginator = Paginator(properties, 6)  # Show 6 properties per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    #Property Search Form
    form = SearchPropertyForm(request.GET)
    if form.is_valid():
        value = form.cleaned_data['value']
        properties = properties.filter(Q(property_type__icontains=value) | Q(address__icontains=value) | Q(state__icontains=value))
        if not properties:
            messages.info(request, 'No properties match your search query.')

     # Paginate the properties
    paginator = Paginator(properties, 6)  # Show 6 properties per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
         'form': form,
         'properties': page_obj,
        'page_title': f'{user_type} Property Listing',
        'total_properties': paginator.count,
    }
    return render(request, 'realestate/listings.html', context)




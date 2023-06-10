from django.shortcuts import render, redirect,  get_object_or_404
from . models import *
from . forms import *
from account.models import *
from django.contrib.auth import logout
from django.utils.crypto import constant_time_compare
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user
from django.db.models import Q
from django.core.paginator import Paginator
from geopy.distance import *
from django.urls import reverse
# Create your views here.
#Add Property View

@login_required(login_url='account-login')
def add_property(request):
    properties = {}
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
    user = request.user
    #Check if user is authenticated
    if user.is_authenticated:
        #Check if user is Landlord
        if user.landlord:
            properties = Property.objects.filter(landlord=user.landlord).prefetch_related('agent').order_by('-last_updated')[:4]
            property_owner = user.landlord
        #Check if user is Agent
        elif user.agent:
            properties = Property.objects.filter(agent=user.agent).prefetch_related('landlord').order_by('-last_updated')[:4]
            property_owner = user.agent
        else:
            properties = Property.objects.order_by('-last_updated')[:4]
            property_owner = None
    
        #Get the Property by its Product key from DB
        property_instance = get_object_or_404(Property, pk=property_id)

        #Send Notification to property owner
        if request.method == 'POST':
            form = PropertyInquiryForm(request.POST)
            if form.is_valid():
                    prospect = request.user.prospect_profile
                    message = form.cleaned_data['message']
                    subject = form.cleaned_data['subject']
                    Notification.objects.create(property=property_instance, prospect=prospect, subject=subject, message=message)
                    messages.success(request, 'Notification sent successfully with your Contact Details.')
    
        else:
            form = PropertyInquiryForm()
            
        context = {
            'form':form,
            'properties':properties,
            'property_owner': property_owner,
            'page_title': 'Property Detail',
            'property': property_instance,
        }
        return render(request, 'realestate/landlord_agent_property.html', context)
     # Handle the case when the user is not authenticated
    logout(request)
    messages.warning(request, 'Session expired. Please log in again.')
    return redirect(reverse('account-login'))

#Landlord and agents prospects
@login_required(login_url='account-login')
def landlord_agents_prospects(request):
    user_type = request.session.get('user_type')
    if user_type is None:
        logout(request)
        messages.warning(request, 'Session expired. Please log in again.')
        return redirect('account-login')  # Replace 'login' with your actual login URL
    #Set logged in user variable
    user = request.user
    if user_type == 'landlord':
        # Get all the landlord notifications 
        notifications = Notification.objects.filter(property__landlord=user.landlord).order_by('-date')
    elif user_type == 'agent':
        # Get all the Agent notifications
        notifications = Notification.objects.filter(property__agent=user.agent).order_by('-date')
   
    else:
        # Handle the case when the user type is not recognized
        return redirect('account-login')
    
    # Paginate the notifications
    paginator = Paginator(notifications, 6)  # Show 6 Messages per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_title': 'Prospects',
        'notifications':page_obj,
    }
    return render(request, 'realestate/landlord_agent_prospect.html', context)

#Landlord and Agent Read Notification and send message
@login_required(login_url='account-login')
def notification_message(request, notification_id):
    user_type = request.session.get('user_type')
    if user_type is None:
        logout(request)
        messages.warning(request, 'Session expired. Please log in again.')
        return redirect('account-login')  # Replace 'login' with your actual login URL
    #Get the Notification by its product key
    notification_instance = get_object_or_404(Notification, pk=notification_id)
    notification_instance.status = True  # Update the status field to True
    notification_instance.save() #Save the update

    if request.method == 'POST':
        form = PropertyInquiryForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            subject = form.cleaned_data['subject']
            prospect = notification_instance.prospect  # Get the associated prospect
            Message.objects.create(property=notification_instance.property, prospect=prospect, subject=subject, message=message)
            messages.success(request, f'Notification sent to {prospect} successfully.')
    else:
        form = PropertyInquiryForm()
    context = {
        'notification': notification_instance,
        'page_titile':'Prospect Message',
        'form':form,
    }
    
    return render(request, 'realestate/notification.html', context)

#Prospect Notifications
@login_required(login_url='account-login')
def prospect_notification(request):
    user_type = request.session.get('user_type')
    if user_type is None:
        logout(request)
        messages.warning(request, 'Session expired. Please log in again.')
        return redirect('account-login')  # Replace 'login' with your actual login URL
    #Set logged in user variable
    user = request.user
    if user_type == 'prospect':
        # Get all the prospect notification  
        notifications = Message.objects.filter(prospect__user=user).order_by('-date')
    else:
        # Handle the case when the user type is not recognized
        return redirect('account-login')
    
    # Paginate the notifications
    paginator = Paginator(notifications, 6)  # Show 6 Messages per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_title': 'Prospect Messages',
        'notifications':page_obj,
    }
    return render(request, 'realestate/prospect_notification.html', context)

#Prospect Read Message
@login_required(login_url='account-login')
def prospect_read_message(request, message_id):
    user_type = request.session.get('user_type')
    if user_type is None:
        logout(request)
        messages.warning(request, 'Session expired. Please log in again.')
        return redirect('account-login')  # Replace 'login' with your actual login URL
    #Get the Notification by its product key
    notification_instance = get_object_or_404(Message, pk=message_id)
    notification_instance.status = True  # Update the status field to True
    notification_instance.save() #Save the update

    if request.method == 'POST':
        form = PropertyInquiryForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            subject = form.cleaned_data['subject']
            prospect = notification_instance.prospect  # Get the associated prospect
            Notification.objects.create(property=notification_instance.property, prospect=prospect, subject=subject, message=message)
            messages.success(request, f'Notification sent successfully.')
    else:
        form = PropertyInquiryForm()
    context = {
        'notification': notification_instance,
        'page_titile':'Prospect Message',
        'form':form,
    }
    
    return render(request, 'realestate/prospect_message.html', context)

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
    
    # Get user's current latitude and longitude from the request object
    user_latitude = request.GET.get('latitude')
    user_longitude = request.GET.get('longitude')

    #Get all listed properties
    properties = Property.objects.order_by('-last_updated')

    # Calculate distances and filter nearby properties
    nearby_properties = []
    
    if user_latitude and user_longitude:
        user_location = (user_latitude, user_longitude)
        
        for property in properties:
            property_location = (property.latitude, property.longitude)
            distance = geodesic(user_location, property_location).miles
            
            # Adjust the distance threshold as needed
            if distance <= 10:  # Filter properties within 10 miles
                nearby_properties.append(property)

    # Paginate the properties
    paginator = Paginator(nearby_properties, 6)  # Show 6 properties per page
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




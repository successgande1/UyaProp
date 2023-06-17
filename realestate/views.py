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
from django.contrib.auth import get_user_model
# Create your views here.
#Add Property View

def custom_page_not_found(request, exception=None):
    return render(request, 'realestate/404.html', status=404)

@login_required(login_url='account-login')
def add_property(request):
    properties = {}
    # Get logged in user
    user = request.user
    #Check if user is landlord or agent
    if not user.is_authenticated:
        logout(request)
        messages.warning(request, 'Session expired. Please log in again.')
        return redirect('account-login')
    #Check form and submit
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property_instance = form.save(commit=False)

            # Set the appropriate Landlord or Agent based on user login type
            if hasattr(user, 'landlord'):
                property_instance.landlord = request.user.landlord
            elif hasattr(user, 'agent'):
                property_instance.agent = request.user.agent

            property_instance.save()
            return redirect('property_detail', property_id=property_instance.pk)
    else:  # Move the else statement here
        # Get check and get properties of the current user
        if hasattr(user, 'landlord'):
            properties = Property.objects.filter(landlord__user=request.user).prefetch_related('agent').order_by('-last_updated')[:6]
        elif hasattr(user, 'agent'):
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


#Landlord, Agent and Prospect Property Detail and Send Message to Property Owner by Prospct
@login_required(login_url='account-login')
def property_detail(request, property_id):
    user = request.user
    #Check if user is authenticated 
    if not user.is_authenticated:
        logout(request)
        messages.warning(request, 'Session expired. Please log in again.')
        return redirect('account-login')  # Replace 'login' with your actual login URL
    
    property_instance = get_object_or_404(Property, pk=property_id)

    properties = []  # Initialize 'properties' as an empty list

    property_owner = None

    # Get the properties for the current user
    if hasattr(user, 'landlord'):
        properties = Property.objects.filter(landlord__user=request.user).prefetch_related('agent').order_by('-last_updated')[:4]
        
    elif hasattr(user, 'agent'):
        properties = Property.objects.filter(agent__user=request.user).prefetch_related('landlord').order_by('-last_updated')[:4]
    
    #Get prospect user profile   
    elif hasattr(user, 'prospect_profile'):
        properties = Property.objects.order_by('-last_updated')[:4]
        if property_instance.landlord:
            property_owner = property_instance.landlord
        elif property_instance.agent:
            property_owner = property_instance.agent
            
       
    context = {
        
        'properties':properties,
        'property_owner': property_owner,
        'page_title': 'Property Detail',
        'property': property_instance,
    }
    return render(request, 'realestate/property_detail.html', context)

#User Send Message
def send_message(request, property_id, recipient_id):
    property = get_object_or_404(Property, id=property_id)
    recipient = get_object_or_404(User, id=recipient_id)

    try:
        recipient = User.objects.get(id=recipient_id)
    except User.DoesNotExist:
        # Handle the case when the recipient doesn't exist
        message.warning(request, 'Recipient Does Not Exist.')
        return redirect('account-login')  # Or re
    
    # if property.landlord_id == recipient_id:
    #     recipient = property.landlord.user
    # elif property.agent_id == recipient_id:
    #     recipient = property.agent.user
   
    
    # if recipient is None:
    #     # Handle the case where the recipient is not found
    #     # Redirect or show an error message
    #     return redirect('home')  # Or return an error response
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['content']
            subject = form.cleaned_data['subject']
            
            message = Message(sender=request.user, recipient=recipient, subject=subject, content=message, property=property)
            message.save()
            messages.success(request, 'Message sent successfully.')
            return redirect('inbox')
        
    else:
        form = MessageForm()
       
    context = {
        'form': form,
        'page_title': 'Send Message',
        'recipient': recipient,
    }
    
    return render(request, 'realestate/send_message.html', context)

#All users Inbox messages
@login_required(login_url='account-login')
def inbox(request):
    user = request.user
    if not user.is_authenticated:
        logout(request)
        messages.warning(request, 'Session expired. Please log in again.')
        return redirect('account-login') 
    
    received_messages = Message.objects.filter(recipient=request.user).order_by('-date')

    #Paginate inbox messages
    paginator = Paginator(received_messages, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'messages': page_obj,
        'page_title':'Inbox',
        }
    return render(request, 'realestate/inbox.html', context)

#user Read and send message
@login_required(login_url='account-login')
def read_message(request, message_id):
    user = request.user
    if not user.is_authenticated:
        logout(request)
        messages.warning(request, 'Session expired. Please log in again.')
        return redirect('account-login') 
    
    #Get the Message by its product key
    message_instance = get_object_or_404(Message, pk=message_id)
    message_instance.mark_as_read()  # Update the status of the Message as Read

    # Access the sender's details
    sender_details = message_instance.sender.profile
    property_id = message_instance.property_id #Get the property ID
    

    
    context = {
        'notification': message_instance,
        'page_titile':'Prospect Message',
        'sender_details': sender_details,
        'page_title': 'Read Message',
        'property_id':property_id,
        
    }
    
    return render(request, 'realestate/message_content.html', context)

#Prospect List Messages View
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
        # Get all the prospect Messages  
        notifications = Message.objects.filter(recipient=user).order_by('-date')
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
    return render(request, 'realestate/inbox.html', context)

#Prospect Read and Reply Message View
@login_required(login_url='account-login')
def prospect_read_message(request, message_id):
    user_type = request.session.get('user_type')
    if user_type is None:
        logout(request)
        messages.warning(request, 'Session expired. Please log in again.')
        return redirect('account-login')  # Replace 'login' with your actual login URL
    #Get the Notification by its product key
    notification_instance = get_object_or_404(Message, pk=message_id)
    notification_instance.mark_as_read()  # Update the status field to True
   

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['content']
            subject = form.cleaned_data['subject']
            prospect = notification_instance.recipient  # Get the associated prospect
            Message.objects.create(property=notification_instance.property, sender=prospect, recipient=notification_instance.sender, subject=subject, content=message)
            messages.success(request, f'Message sent successfully to {notification_instance.sender}.')
    else:
        form = MessageForm()
    context = {
        'notification': notification_instance,
        'page_title':'Prospect Message',
        'form':form,
    }
    
    return render(request, 'realestate/prospect_message.html', context)

#Delete Message View
@login_required(login_url='account-login')
def delete_message(request,pk):
    #Get the session user type
    user_type = request.session.get('user_type')
    #Check if user type is NOT in the session and logout the user
    if user_type is None:
        logout(request)
        messages.warning(request, 'Session expired. Please log in again.')
        return redirect('account-login')  
    
    message_item = Message.objects.get(id=pk)
    if request.method == "POST":
        message_item.delete()
        message_descrip = message_item.subject
        
        messages.error(request, f'{message_descrip} Message Item on {message_item.property} Deleted successfully')
        
        if user_type == 'landlord' or user_type == 'agent':
            return redirect('landlord-agent-prospects')
        else:
            return redirect('prospect-notification')
    context = {
        'message_item':message_item,
        'page_title':'Delete Message',
    }
    return render(request, 'realestate/delete_message.html', context)

#Delete Multiple Messages View
@login_required(login_url='account-login')
def delete_multiple_messages(request):
    user_type = request.session.get('user_type')
    if user_type is None:
        logout(request)
        messages.warning(request, 'Session expired. Please log in again.')
        return redirect('account-login')
    
    if request.method == "POST":
        message_ids = request.POST.getlist('message_ids')
        messages_deleted = []
        
        for message_id in message_ids:
            message_item = Message.objects.get(id=message_id)
            message_item.delete()
            messages_deleted.append(message_item.subject)
        
        if len(messages_deleted) > 0:
            messages.success(request, f'{len(messages_deleted)} messages deleted successfully')
        
        if user_type == 'landlord' or user_type == 'agent':
            return redirect('landlord-agent-prospects')
        else:
            return redirect('prospect-notification')
    
    return redirect('delete-message')


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




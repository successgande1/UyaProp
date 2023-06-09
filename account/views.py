from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from . forms import *
from realestate.models import *
from . models import *
from django.contrib.auth.decorators import login_required
from geopy.geocoders import Nominatim
from realestate.models import *
from django.contrib.sessions.models import Session
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth import authenticate, update_session_auth_hash




#Register New User Method
def register(request):
    if request.user.is_authenticated:
        return redirect('account-dashboard')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_type = form.cleaned_data['user_type']
            
            if user_type == 'landlord':
                Landlord.objects.create(user=user)
            elif user_type == 'agent':
                Agent.objects.create(user=user)
            elif user_type == 'prospect':
                Prospect.objects.create(user=user)

            #login(request, user)
            messages.success(request, 'Registered successfully.')
            return redirect('account-login')
    else:
        form = RegistrationForm()
    
    context = {
        'form': form,
        'page_title': 'Register',
    }
    return render(request, 'account/register.html', context)

#User Login View
class MyLoginView(LoginView):
    template_name = 'account/login.html'
    form_class = UserLoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'User Login'  # Set the page title
        return context

    def form_valid(self, form):
        user = form.get_user()
        user_type = form.cleaned_data['user_type']

        # Get the user's associated profile based on the selected user type
        if user_type == 'landlord':
            profile = getattr(user, 'landlord', None)
        elif user_type == 'agent':
            profile = getattr(user, 'agent', None)
        elif user_type == 'prospect':
            profile = getattr(user, 'prospect_profile', None)
        else:
            profile = None

        # Check if the user's profile matches the selected user type
        if profile is None:
            form.add_error('user_type', 'Invalid user type for this user.')
            return self.form_invalid(form)

        # Authenticate the user
        login(self.request, user)

        # Set user type in the session
        self.request.session['user_type'] = user_type

        return super().form_valid(form)
    


#User Dashboard Index
@login_required(login_url='account-login')
def index(request):
    user = request.user
   
    if user.is_authenticated:
        # Check if User Profile is completed with new image uploaded 
        def profile_complete(profile):
            return (
                profile.full_name is not None and profile.full_name != '' and
                profile.phone_number is not None and profile.phone_number != '' and
                profile.email is not None and profile.email != '' and
                profile.address is not None and profile.address != '' and
                profile.image is not None and profile.image != 'avatar.jpg'
            )
        #Check if user is either a Landlord, Agent, or Prospect and Profile is completed and they have unread messages
        if hasattr(user, 'landlord') or hasattr(user, 'agent'):
            try:
                profile = Profile.objects.select_related('user').get(user=user)
                if not profile_complete(profile):
                    return redirect('account-profile-update')
                elif hasattr(user, 'landlord'):
                    # Get all logged in landlord Properties
                    landlord_properties = Property.objects.filter(landlord__user=user)
                    if not landlord_properties.exists():
                        return redirect('add-property')
                    # Check if landlord has any notifications with status False
                    elif Message.objects.filter(property__landlord=user.landlord, status=False).exists():
                        return redirect('inbox')
                    else:
                        return redirect('property-listing')
                elif hasattr(user, 'agent'):
                    # Get all the logged in Agent Properties
                    agent_properties = Property.objects.filter(agent__user=user)
                    if not agent_properties.exists():
                        return redirect('add-property')
                    # Check ifagent has any notifications with status False
                    elif Message.objects.filter(property__agent=user.agent, status=False).exists():
                        return redirect('inbox') 
                    else:
                        return redirect('property-listing')
            except (Landlord.DoesNotExist, Agent.DoesNotExist): 
                pass
        #Check if user is Prospect and Profile is completed
        elif hasattr(user, 'prospect_profile'):
            try:
                #Match the logged in user with users in the Profile DB
                prospect_profile = Profile.objects.get(user=user)
                #Check if Prospect Profile is completed and redirect
                if not profile_complete(prospect_profile):
                    return redirect('account-profile-update')
                elif Message.objects.filter(recipient=user, status=False).exists():
                    return redirect('inbox')
                else:
                    return redirect('listings')
            except Prospect.DoesNotExist:
                pass
    
    request.session['user_type'] = 'default'
    return redirect('account-login')

    
#View User Profile Method
@login_required(login_url='account-login')
def update_profile(request):
    user = request.user
    profile = user.profile
    #Check whether user is logged in
    if not user.is_authenticated:
        logout(request)
        messages.warning(request, 'Session expired. Please log in again.')
    #Check and submit form
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            #Check user roles and redirect accordingly
            if hasattr(user, 'landlord') or hasattr(user, 'agent'):
                messages.success(request, 'Profile updated Successfully')
                return redirect('add-property')
            elif hasattr(user, 'prospect_profile'):
                messages.success(request, 'Profile updated Successfully')
                return redirect('listings')
            else:
                return redirect('account-dashboard')
    else:
        form = ProfileForm(instance=profile)

    #Count unread messages
    unread_message_count = Message.objects.filter(recipient=request.user, status=False).count()

    context = {
        'unread_message_count':unread_message_count,
        'form': form,
        'page_title':'Update Profile',
    }

    return render(request, 'account/update_profile.html', context)
    
#User Profile Method
@login_required(login_url='account-login')
def user_profile(request):
    
    #Count unread messages
    unread_message_count = Message.objects.filter(recipient=request.user, status=False).count()

    context = {
        'unread_message_count':unread_message_count,
        'page_title': f'{request.user.username} Profile',
    }
    return render(request, 'account/profile_detail.html', context)

#Landlord Landing Page
@login_required(login_url='account-login')
def landlord_dashboard(request):
    context = {
        'page_title':'Landlord Dashboard',
    }
    return render(request, 'account/landload_dashboard.html', context)

#Agent Landing Page
@login_required
def agent_dashboard(request):
    context = {
        'page_title':'Agent Dashboard',
    }
    return render(request, 'account/agent_dashboard.html', context)

#Prospect Landing Page
@login_required
def prospect_dashboard(request):
    context = {
        'page_title':'Prospect Dashboard',
    }
    return render(request, 'account/prospect_dashboard.html', context)

#Default Landing Page
@login_required
def default_dashboard(request):
    context = {
        'page_title':'Default Dashboard',
    }
    return render(request, 'account/default_dashboard.html', context)

#Change user password view
@login_required(login_url='account-login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            user = authenticate(username=request.user.username, password=form.cleaned_data['old_password'])
            if user is not None:
                user.set_password(form.cleaned_data['new_password'])
                user.save()
                update_session_auth_hash(request, user)  # Update session to prevent logout
                messages.success(request, 'Your Password Changed Successfully.')
                return redirect('password_change_done')  # Redirect to password change success page
            else:
                form.add_error('old_password', 'Incorrect old password')
                messages.warning(request, 'Incorrect old Password.')
    else:
        form = PasswordChangeForm()

    context = {
        'form': form,
        'page_title': 'Change Password',
        }
    return render(request, 'account/password_change.html', context)

#Change user password successfully view
@login_required(login_url='account-login')
def password_change_done(request):

    context = {
        'page_title':'Password Changed',
    }
    return render(request, 'account/password_change_done.html', context)

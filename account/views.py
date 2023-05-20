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



#Register New User Method
def register(request):
    if request.user.is_authenticated:
        return redirect('account-dashboard')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Create a new user object
            user = form.save()
            # Get the user_type value from the form
            user_type = form.cleaned_data['user_type']
            # Create a new object based on the user_type
            if user_type == 'landlord':
                Landlord.objects.create(user=user)
            elif user_type == 'agent':
                Agent.objects.create(user=user)
            elif user_type == 'prospect':
                Prospect.objects.create(user=user)

            # Set user_type as a session variable
            request.session['user_type'] = user_type

            # Log the user in and redirect to the homepage
            login(request, user)
            return redirect('account-dashboard')
    else:
        form = RegistrationForm()
    context =  {
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

        # Check if the selected user type matches the user's actual user type
        if user_type == 'landlord' and not hasattr(user, 'landlord'):
            form.add_error('user_type', 'Invalid user type for this user.')
            return self.form_invalid(form)
        elif user_type == 'agent' and not hasattr(user, 'agent'):
            form.add_error('user_type', 'Invalid user type for this user.')
            return self.form_invalid(form)
        elif user_type == 'prospect' and not hasattr(user, 'prospect_profile'):
            form.add_error('user_type', 'Invalid user type for this user.')
            return self.form_invalid(form)

        # Authenticate the user
        login(self.request, user)

        # Set user type in the session
        self.request.session['user_type'] = user_type

        return super().form_valid(form)

    


#User Dashboard Index
@login_required
def index(request):
    user = request.user
    user_type = request.session.get('user_type')

    if user_type:
        # Check if User Profile is completed and redirect appropriately
        def profile_complete(profile):
            return (
                profile.full_name is not None and profile.full_name != '' and
                profile.phone_number is not None and profile.phone_number != '' and
                profile.email is not None and profile.email != '' and
                profile.address is not None and profile.address != '' and
                profile.image is not None
            )

        if user_type == 'landlord':
            try:
                landlord_profile = Profile.objects.get(user=user)
                if not profile_complete(landlord_profile):
                    return redirect('account-profile-update')
                else:
                    return redirect('landlord-dashboard')
            except Profile.DoesNotExist:
                pass

        elif user_type == 'agent':
            try:
                agent_profile = Profile.objects.get(user=user)
                if not profile_complete(agent_profile):
                    return redirect('account-profile-update')
                else:
                    return redirect('agent-dashboard')
            except Agent.DoesNotExist:
                pass

        elif user_type == 'prospect':
            try:
                prospect_profile = Profile.objects.get(user=user)
                if not profile_complete(prospect_profile):
                    return redirect('account-profile-update')
                else:
                    return redirect('prospect-dashboard')
            except Prospect.DoesNotExist:
                pass

    request.session['user_type'] = 'default'
    return redirect('account-login')


        




    
#View User Profile Method
@login_required
def update_profile(request):
    user = request.user
    profile = user.profile

    # Check the user type stored in the session
    user_type = request.session.get('user_type')

    if not user_type:
        # If user type is not set, redirect to the index view to set the session
        return redirect('account-dashboard')
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            
            return redirect('account-profile')
    else:
        form = ProfileForm(instance=profile)

    context = {
        'form': form,
    }

    return render(request, 'account/update_profile.html', context)
    
#User Profile Method
@login_required
def user_profile(request):
    context = {
        'page_titel': 'Profile',
    }
    return render(request, 'account/profile_detail.html', context)

#Landlord Landing Page
@login_required
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
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Define the user_type choices
USER_TYPE_CHOICES = (
    ('landlord', 'Landlord'),
    ('agent', 'Agent'),
    ('prospect', 'Prospect'),
)

# Create the registration form
class RegistrationForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES)
    
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'user_type']

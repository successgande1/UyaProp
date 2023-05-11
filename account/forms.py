from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

# Define the user_type choices
USER_TYPE_CHOICES = (
    ('landlord', 'Landlord'),
    ('agent', 'Agent'),
    ('prospect', 'Prospect'),
)

# Create the registration form
class RegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control left-label'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control left-label'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control left-label'}))
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, widget=forms.Select(attrs={'class': 'form-control left-label'}))
   
    
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'user_type']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    
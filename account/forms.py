from django import forms
from django.contrib.auth.models import User

USER_TYPE_CHOICES = (
    ('Landlord', 'Landlord'),
    ('Agent', 'Agent'),
    ('Prospect', 'Prospect'),
)

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES)

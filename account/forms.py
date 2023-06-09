from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from PIL import Image
from io import BytesIO
from . models import *
from django.contrib.auth.forms import AuthenticationForm


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
    

class UserLoginForm(AuthenticationForm):
    user_type = forms.ChoiceField(
        choices=USER_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control left-label'}),
    )

    

#Profile Update Form 
class ProfileForm(forms.ModelForm):
    full_name = forms.CharField(label = 'Full Name:', max_length=36, widget=forms.TextInput(attrs={'placeholder': 'Enter Your Full Name'}))
    email = forms.CharField(label = 'Email Address:', max_length=36, widget=forms.TextInput(attrs={'placeholder': 'Enter a Valid Email Address'}))
    phone_number = forms.CharField(label = 'Phone Number:', max_length=11, widget=forms.TextInput(attrs={'placeholder': 'Enter Your 11 Digits Phone Number.'}))
    state = forms.CharField(label = 'State:', max_length=12, widget=forms.TextInput(attrs={'placeholder': 'Enter State  of Residence Name Only.'}))
    address = forms.CharField(label = 'Residential Address:', max_length=60, widget=forms.TextInput(attrs={'placeholder': 'Enter Street Name with Number (where applicable) and Town Name only.'}))
    class Meta:
        model = Profile
        fields = ['full_name', 'phone_number', 'email', 'country', 'state', 'address', 'image']
    
    def clean_image(self):
        image = self.cleaned_data.get('image') 

        if image:
            # Check if the image size exceeds 14kb
            if image.size > 14 * 1024:  # 14kb in bytes
                # Open the image using Pillow
                with Image.open(image) as img:
                    # Resize the image while preserving the aspect ratio
                    max_size = (img.width, img.height)
                    img.thumbnail(max_size)

                    # Rotate the image if it's originally landscape
                    if img.width > img.height:
                        img = img.transpose(Image.ROTATE_90)

                    # Save the modified image back to the InMemoryUploadedFile object
                    buffer = BytesIO()
                    img.save(buffer, format='JPEG')
                    image.file = buffer

            # Check file extension for allowed formats
            allowed_formats = ['gif', 'jpeg', 'jpg']
            ext = image.name.split('.')[-1].lower()
            if ext not in allowed_formats:
                raise forms.ValidationError("Only GIF, JPEG, and JPG images are allowed.")
            
            # Check if the image is still set to the default 'avatar.jpg'
            if image.name == 'avatar.jpg':
                raise forms.ValidationError("Please upload a different image before submitting the form.")

        return image
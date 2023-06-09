from django import forms

from PIL import Image
from io import BytesIO
from .models import Property
import os
from django.core.exceptions import ValidationError



ALLOWED_EXTENSIONS = ('.gif', '.jpg', '.jpeg')

class PropertyForm(forms.ModelForm):
    description = forms.CharField(label='Property Description:', max_length=60, widget=forms.TextInput(attrs={'placeholder': 'Briefly Describe your Property. E.g. Bedroom & Palour with Private Detached Bathroom'}))
    state = forms.CharField(label='State Residence:', max_length=10, widget=forms.TextInput(attrs={'placeholder': 'Enter State of Property'}))
    state_lga = forms.CharField(label = 'Local Govt. Area:', max_length=12, widget=forms.TextInput(attrs={'placeholder': 'Enter Local Govt. of Property.'}))
    address = forms.CharField(label = 'Property Address:', max_length=60, widget=forms.TextInput(attrs={'placeholder': 'Enter Street Name with Number and Town Name only.'}))
    class Meta:
        model = Property
        fields = ('description', 'address', 'country', 'state', 'state_lga', 'property_type', 'bedrooms', 'bathroom_type', 'price', 'is_available', 'image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bedrooms'].required = False


def clean_image(self):
    image = self.cleaned_data.get('image')

    if image:
        # Check if the image size exceeds 1MB
        if image.size > 1024 * 1024:  # 1MB in bytes
            # Open the image using Pillow
            with Image.open(image) as img:
                # Reduce the image size while preserving the aspect ratio
                max_width = 1920
                max_height = 820
                img.thumbnail((max_width, max_height), Image.ANTIALIAS)

                # Save the modified image with reduced quality to achieve a smaller file size
                buffer = BytesIO()
                img.save(buffer, format='JPEG', optimize=True, quality=85)
                while buffer.tell() > 1024 * 1024:  # Check if file size exceeds 1MB
                    quality -= 5
                    if quality < 5:
                        break
                    buffer.seek(0)
                    buffer.truncate(0)
                    img.save(buffer, format='JPEG', optimize=True, quality=quality)

                buffer.seek(0)
                image.file = buffer

        # Check file extension for allowed formats
        allowed_formats = ['gif', 'jpeg', 'jpg']
        ext = image.name.split('.')[-1].lower()
        if ext not in allowed_formats:
            raise forms.ValidationError("Only GIF, JPEG, and JPG images are allowed.")
        
        # Check if the image is still set to the default 'avatar.jpg'
        # if image.name == 'avatar.jpg':
        #     raise forms.ValidationError("Please upload a different image before submitting the form.")
    else:
        raise forms.ValidationError("Please upload an image before submitting the form.")

    return image
    
#Search Landlord and Agent Property form
class SearchPropertyForm(forms.Form):
    value = forms.CharField(label = 'Search by Address or Property Type', max_length=30)


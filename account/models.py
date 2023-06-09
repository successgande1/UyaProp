from django.db import models
from django.contrib.auth.models import User

from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent='Successgande-uyaprop')
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, Adjust, Transpose
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from PIL import Image
from imagekit.models import ProcessedImageField


class Profile(models.Model):
    COUNTRY_CHOICES = [
        ('Nigeria', 'Nigeria'),
        
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=30, blank=True, null=True)
    phone_number = models.CharField(max_length=11, blank=True, null=True)
    email = models.EmailField()
    country = models.CharField(max_length=20, choices=COUNTRY_CHOICES)
    state = models.CharField(max_length=20, blank=True, null=True)
    town = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    image = models.ImageField(default='avatar.jpg', blank=False, null=False, upload_to ='profile_images', 
    )

    # #Method to save Image
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     img = Image.open(self.image.path)
    # #Check for Image Height and Width then resize it then save
    #     if img.height > 200 or img.width > 150:
    #         output_size = (150, 250)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)
            
    # Method for saving latitude and lingitude
    def save(self, *args, **kwargs):
        location = geolocator.geocode(self.address)
        if location:
            self.latitude = location.latitude
            self.longitude = location.longitude
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username

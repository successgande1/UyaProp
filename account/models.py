from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(default='avatar.jpg', blank=False, null=False, upload_to ='profile_images', 
   
    )
    # Add any additional fields as needed

    def __str__(self):
        return self.user.username

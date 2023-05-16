from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=30, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField()
    address = models.TextField(null=True, blank=True)
    image = models.ImageField(default='avatar.jpg', blank=False, null=False, upload_to ='profile_images', 
   
    )
    # Add any additional fields as needed

    def __str__(self):
        return self.user.username

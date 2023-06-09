from django.db import models
from django.contrib.auth.models import User
#from django.contrib.gis.db import models
# from django.contrib.gis.geos import Point
import requests
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from PIL import Image
from geopy.geocoders import Nominatim
from imagekit.models import ProcessedImageField
geolocator = Nominatim(user_agent='Successgande-uyaprop')




class Landlord(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False) 

    def __str__(self):
        return self.user.username

  

class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

@deconstructible
class AllowedFormatsValidator:
    def __call__(self, value):
        image = Image.open(value)
        if image.format not in ['JPEG', 'JPG', 'PNG']:
            raise ValidationError("Only JPEG, JPG, and PNG formats are allowed.")
        


class Property(models.Model):
    PROPERTY_TYPE_CHOICES = [
        ('Complete House', 'Complete House'),
        ('One Room Apartment', 'One Room Apartment'),
        ('Bedroom & Palour', 'Bedroom & Palour'),
        ('Bedroom & Palour Self-Contained', 'Bedroom & Palour Self-Contained'),
        ('One Room Self-Contained', 'One Room Self-Contained'),
       
        
    ]

    BEDROOM_CHOICES = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5+'),
    ]

    BATHROOM_CHOICES = [
        ('Self-contained', 'Self-contained'),
        ('General', 'General'),
        ('Private Detached', 'Private Detached'),
    ]

    COUNTRY_CHOICES = [
        ('Nigeria', 'Nigeria'),
        
    ]

    STATE_CHOICES = [
        ('Abia', 'Abia'),
        ('Adamawa', 'Adamawa'),
        ('Akwa Ibom', 'Akwa Ibom'),
        ('Anambra ', 'Anambra '),
        ('Bauchi', 'Bauchi'),
        ('Bayelsa', 'Bayelsa'),
        ('Benue ', 'Benue '),
        ('Borno', 'Borno'),
        ('Cross River', 'Cross River'),
        ('Delta', 'Delta'),
        ('Ebonyi', 'Ebonyi'),
        ('Edo', 'Edo'),
        ('Ekiti', 'Ekiti'),
        ('Enugu', 'Enugu'),
        ('Gombe', 'Gombe'),
        ('Imo', 'Imo'),
        ('Jigawa', 'Jigawa'),
        ('Kaduna', 'Kaduna'),
         ('Kano', 'Kano'),
        ('Katsina', 'Katsina'),
        ('Kebbi', 'Kebbi'),
        ('Kogi', 'Kogi'),
        ('Kwara', 'Kwara'),
        ('Lagos', 'Lagos'),
        
    ]

    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, blank=True, null=True)
    landlord = models.ForeignKey(Landlord, on_delete=models.SET_NULL, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    property_type = models.CharField(max_length=100, choices=PROPERTY_TYPE_CHOICES)
    bedrooms = models.CharField(max_length=2, blank=True, null=True, choices=BEDROOM_CHOICES)
    bathroom_type = models.CharField(max_length=60, choices=BATHROOM_CHOICES)
    country = models.CharField(max_length=20, choices=COUNTRY_CHOICES)
    state = models.CharField(max_length=20, choices=STATE_CHOICES)
    town = models.CharField(max_length=12, blank=True, null=True)
    address = models.CharField(max_length=60, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    #image = models.ImageField(upload_to ='profile_images', blank=False, null=False, validators=[AllowedFormatsValidator()])
    image = ProcessedImageField(upload_to='profile_images',
                                           processors=[ResizeToFill(1920, 850)],
                                           format='JPEG',
                                           options={'quality': 60})
    
    last_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description
    
    # def save(self, *args, **kwargs):
    #     if not self.pk:
    #         self.generate_thumbnail()
    #     super().save(*args, **kwargs)

    # def generate_thumbnail(self):
    #     image = Image.open(self.image)
    #     image.thumbnail((1920, 820))
    #     thumbnail_path = self.thumbnail.storage.path(self.thumbnail.name)
    #     image.save(thumbnail_path, 'JPEG', quality=60)

    

class Prospect(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='prospect_profile')
    payment_ref = models.CharField(max_length=100, blank=True, null=True)
    payment_status = models.BooleanField(default=False)
    properties = models.ManyToManyField('Property', through='Tenancy')


    def __str__(self):
        return self.user.username
    
    def become_tenant(self, property):
        if self.payment_status:
            tenant = Tenancy.objects.create(tenant=self, property=property, agent=property.agent, landlord=property.landlord)
            return tenant
        else:
            return None
    
class Tenancy(models.Model):
    tenant = models.ForeignKey(Prospect, on_delete=models.CASCADE)
    property = models.ForeignKey('Property', on_delete=models.CASCADE)
    agent = models.ForeignKey('Agent', on_delete=models.CASCADE)
    landlord = models.ForeignKey('Landlord', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f'{self.tenant} - {self.property}'

    class Meta:
        verbose_name_plural = 'Tenancies'

class Payment(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    prospect = models.ForeignKey(Prospect, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_reference = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.prospect} - {self.property}'
    
class Message(models.Model):
    SUBJECT_CHOICES = [
        ('Inquiry', 'Inquiry'),
        ('Reinquiry', 'Reinquiry'),
        ('Negotiation', 'Negotiation'),
        ('Payment', 'Payment'),
    ]

    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES)
    content = models.TextField(max_length=220, blank=True, null=True)
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.username} - {self.recipient.username}'
    
    def mark_as_read(self):
        self.status = True
        self.save()

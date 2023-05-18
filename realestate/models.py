from django.db import models
from django.contrib.auth.models import User
#from django.contrib.gis.db import models
# from django.contrib.gis.geos import Point
import requests




class Landlord(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nin = models.CharField(max_length=11, unique=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

  

class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nin = models.CharField(max_length=11, unique=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    

class Property(models.Model):
    PROPERTY_TYPE_CHOICES = [
        ('House', 'House'),
        ('Apartment', 'Apartment'),
        ('Condo', 'Condo'),
        ('Duplex', 'Duplex'),
        ('Townhouse', 'Townhouse'),
        ('Other', 'Other'),
    ]
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, blank=True, null=True)
    landlord = models.ForeignKey(Landlord, on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    image = models.ImageField(default='avatar.jpg', blank=False, null=False, upload_to ='profile_images', 
   
    )

    def __str__(self):
        return self.title

    

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
    def __str__(self):
        return f'{self.prospect} - {self.property}'
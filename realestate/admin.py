from django.contrib import admin
from . models import *

# Register your models here.
admin.site.register(Landlord)

admin.site.register(Agent)

admin.site.register(Prospect)

admin.site.register(Tenancy)
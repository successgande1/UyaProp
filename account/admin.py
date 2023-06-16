from django.contrib import admin
from . models import *


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'phone_number', 'address', 'latitude', 'longitude', 'image')
    list_per_page = 20
admin.site.register(Profile, ProfileAdmin)
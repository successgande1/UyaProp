from django.contrib import admin
from . models import *


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'phone_number', 'address', 'image')
    list_per_page = 20
admin.site.register(Profile, ProfileAdmin)
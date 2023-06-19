from django.contrib import admin
from . models import *
# Register your models here.
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'phone', 'content', 'status', 'date')
    list_per_page = 20
admin.site.register(Contact, ContactAdmin)
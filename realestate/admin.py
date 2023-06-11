from django.contrib import admin
from . models import *

# Register your models here.
admin.site.register(Landlord)

admin.site.register(Agent)

admin.site.register(Prospect)

admin.site.register(Tenancy) 

admin.site.register(Property) 

class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'subject', 'content', 'status', 'date')
    list_per_page = 6
admin.site.register(Message, MessageAdmin)
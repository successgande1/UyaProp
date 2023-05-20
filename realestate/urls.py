from django.urls import path
from . import views



urlpatterns = [
   
    path('add/property/', views.add_property, name='add-property'), 
    path('landlord/and/agent/prospects/', views.landlord_agents_prospects, name='landlord-agent-prospects'),
    path('landlord/agent/listing/', views.property_listing, name='property-listing'), 
    path('listings/', views.listings, name='listings'), 
]

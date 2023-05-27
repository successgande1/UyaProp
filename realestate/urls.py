from django.urls import path
from . import views



urlpatterns = [
   
    path('add/property/', views.add_property, name='add-property'), 
    path('property/<int:property_id>/', views.property_detail, name='property_detail'),
    path('landlord/and/agent/prospects/', views.landlord_agents_prospects, name='landlord-agent-prospects'),
    path('landlord/agent/listing/', views.landlord_agent_property_listing, name='property-listing'), 
    path('edit/property/<int:property_id>/', views.edit_property, name='edit-property'), 
    path('listings/', views.listings, name='listings'), 
]

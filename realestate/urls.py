from django.urls import path
from . import views


 
urlpatterns = [
   
    path('add/property/', views.add_property, name='add-property'), 
    path('property/<int:property_id>/', views.property_detail, name='property_detail'),
    path('landlord/and/agent/prospects/', views.landlord_agents_prospects, name='landlord-agent-prospects'),
    path('notification/<int:notification_id>/', views.notification_message, name='message-detail'),
    path('prospect/notification/', views.prospect_notification, name='prospect-notification'),
    path('message/<int:message_id>/', views.prospect_read_message, name='read-message'),
    path('landlord/agent/listing/', views.landlord_agent_property_listing, name='property-listing'), 
    path('edit/property/<int:property_id>/', views.edit_property, name='edit-property'), 
    path('listings/', views.listings, name='listings'), 
]

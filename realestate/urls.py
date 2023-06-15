from django.urls import path
from . import views


 
urlpatterns = [
   
    path('add/property/', views.add_property, name='add-property'), 
    path('property/<int:property_id>/', views.property_detail, name='property_detail'),
    path('send_message/<int:property_id>/<int:recipient_id>/', views.send_message, name='send_message'),
    path('inbox/', views.inbox, name='inbox'),
    # path('landlord/and/agent/prospects/', views.landlord_agents_prospects, name='landlord-agent-prospects'),
    path('read_message/<int:message_id>/', views.read_message, name='message-detail'),
    path('prospect/notification/', views.prospect_notification, name='prospect-notification'),
    path('message/<int:message_id>/', views.prospect_read_message, name='read-message'),
    path('delete/message/<int:pk>/', views.delete_message, name = 'delete-message'),
     path('delete/multiple/messages/', views.delete_multiple_messages, name='delete-multiple-messages'),
    path('landlord/agent/listing/', views.landlord_agent_property_listing, name='property-listing'), 
    path('edit/property/<int:property_id>/', views.edit_property, name='edit-property'), 
    path('listings/', views.listings, name='listings'), 
]

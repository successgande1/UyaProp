from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name = 'pages-index'),
    path('property-management-services/', views.about, name = 'pages-about'),
    path('professional-property-management/', views.services, name = 'pages-services'),
    path('free-property-management/', views.property, name = 'pages-property'),
    path('contact-uyaprop/', views.contact, name = 'pages-contact'),
    path('free-online-property-listing-blog/', views.blog, name = 'pages-blog'),
 
]
   
    

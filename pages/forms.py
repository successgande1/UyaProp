from django import forms
from realestate.filters import PropertyFilter
from realestate.models import Property
from .models import *

class SearchForm(forms.Form):
    property_type = forms.ChoiceField(choices=Property.PROPERTY_TYPE_CHOICES, required=False)
    state = forms.ChoiceField(choices=Property.STATE_CHOICES, required=False)
    min_beds = forms.ChoiceField(choices=Property.BEDROOM_CHOICES, required=False)
    bathroom_type = forms.ChoiceField(choices=Property.BATHROOM_CHOICES, required=False)
    min_price = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    max_price = forms.DecimalField(max_digits=10, decimal_places=2, required=False)

    def search(self):
        queryset = Property.objects.all()
        filter_params = {}

        property_type = self.cleaned_data.get('property_type')
        if property_type:
            filter_params['property_type'] = property_type

        state = self.cleaned_data.get('state')
        if state:
            filter_params['state'] = state

        min_beds = self.cleaned_data.get('min_beds')
        if min_beds:
            filter_params['bedrooms'] = min_beds

        bathroom_type = self.cleaned_data.get('bathroom_type')
        if bathroom_type:
            filter_params['bathroom_type'] = bathroom_type

        min_price = self.cleaned_data.get('min_price')
        if min_price:
            filter_params['price__gte'] = min_price

        max_price = self.cleaned_data.get('max_price')
        if max_price:
            filter_params['price__lte'] = max_price

        return queryset.filter(**filter_params)
    

#Profile Update Form 
class ContactForm(forms.ModelForm): 
    name = forms.CharField(label = 'Full Name:', max_length=36, widget=forms.TextInput(attrs={'placeholder': 'Enter Your Full Name'}))
    email = forms.CharField(label = 'Email Address:', max_length=36, widget=forms.TextInput(attrs={'placeholder': 'Enter a Valid Email Address'}))
    
    phone = forms.CharField(label = 'Phone Number:', max_length=11, widget=forms.TextInput(attrs={'placeholder': 'Enter Valid Phone Number.'}))
    
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'phone', 'content']

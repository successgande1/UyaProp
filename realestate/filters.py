import django_filters
from .models import Property

class PropertyFilter(django_filters.FilterSet):
    class Meta:
        model = Property
        fields = {
            'property_type': ['exact'],
            'state': ['exact'],
            'bedrooms': ['exact'],
            'bathroom_type': ['exact'],
            'price': ['gte', 'lte'],
        }

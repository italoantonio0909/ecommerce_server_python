import django_filters

from .models import Address

class AddressFilter(django_filters.FilterSet):
    class Meta:
        model = Address
        fields = (
            'postal_code',
            'address_type',
            'city',
            'country',
            'is_active'
        )
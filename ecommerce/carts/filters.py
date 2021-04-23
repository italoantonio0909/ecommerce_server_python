import django_filters
from .models import (
    Cart
)


class CartFilter(django_filters.FilterSet):
    class Meta:
        model = Cart
        fields = (
            'user',
            'is_active',
            'total',
            'subtotal'

        )
import django_filters

from .models import (
    Category,
    Product    
)


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = (
            'id',
            'title',
            'description',
            'price',
            'price_discount',
            'category',
        )


class CategoryFilter(django_filters.FilterSet):
    class Meta:
        model = Category
        fields = (
            'id',
            'title',
        )
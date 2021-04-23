from typing import Iterable

from django.core.exceptions import ValidationError

from .filters import CategoryFilter, ProductFilter
from .models import Category, Product


def product_list(*, filters = None):
    filters = filters or {}

    qs = Product.objects.all()

    return ProductFilter(filters, qs).qs


def product_by_id(*, product_id:int) -> Product:
    try:

        return Product.objects.get(id=product_id, is_active=True)

    except Product.DoesNotExist:
        raise ValidationError({'product': 'This product no souch found'})


def category_list(*, filters=None):
    filters = filters or {}
    
    qs = Category.objects.all()
    
    return CategoryFilter(filters, qs).qs
    

def category_by_id(*, category_id: int) -> Category:
    try:

        return Category.objects.get(id=category_id, is_active=True)

    except Category.DoesNotExist:
        raise ValidationError({'product': 'This product no souch found'})



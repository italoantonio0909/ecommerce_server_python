from django.core.exceptions import ValidationError
from django.db import IntegrityError

from .models import Category, Product
from .selectors import (category_by_id, product_by_id)



def product_create(
    *,
    title: str,
    description: str,
    price: float,
    price_discount: float,
    is_active: bool = True,
    category:Category
    ) -> Product:
    
    product = Product(
        title=title,
        description=description,
        price=price,
        price_discount=price_discount,
        category_id=category,
        is_active=is_active
    )
    
    if product.price_discount > product.price:
        raise ValidationError('Discount price cannot be higher than price.')

    product.full_clean()
    product.save()
        
    return product



def product_update(
    *,
    product_id:int,
    data
    ) -> Product:

    valid_fields = [
        'title',
        'description',
        'price',
        'price_discount',
        'category',
        'is_active'
    ]

    # Obtain product
    product = product_by_id(product_id=product_id)

    # Set instance with fields valid in data
    fields = []
    for field in valid_fields:
        if field in data:
            setattr(product, field, data[field])
            fields.append(field)

    if fields:
        product.full_clean()
        
        if product.price_discount > product.price:
            raise ValidationError('Discount price cannot be higher than price.')

        product.save(update_fields=fields)

    return product



def category_create(
    *,
    title: str,
    is_active:bool=True
    ) -> Category:
    
    category = Category(
        title=title,
        is_active=is_active
    )
    category.full_clean()
    category.save()
    
    return category



def category_update(
    *,
    category_id:int,
    data
    ) -> Category:

    valid_fields = [
        'title',
        'is_active'
    ]

    # Category obtain
    category = category_by_id(category_id=category_id)

    fields = []
    for field in valid_fields:
        if field in data:
            setattr(category, field, data[field])
            fields.append(field)
            
    if fields:
        category.full_clean()
        category.save(update_fields=fields)
    
    return category
    


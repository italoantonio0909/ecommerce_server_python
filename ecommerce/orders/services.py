from .models import (
    Order,
    ProductPurchase
)

from ecommerce.carts.models import (
    Cart,
)
from .selectors import (
    order_by_id,
    product_purchase_by_id
)

def order_create(
    *,
    shipping_total=0.0,
    billing_profile_id: int,
    shipping_address_id: int,
    billing_address_id: int,
    shipping_address_final: str = None,
    billing_address_final: str = None,
    cart_id: int,
    total: float = 0.00,
    status: str = 'created',
    is_active:bool=True
    ) -> Order:

    order = Order(
        shipping_total=shipping_total,
        billing_profile_id=billing_profile_id,
        shipping_address_id=shipping_address_id,
        billing_address_id=billing_address_id,
        shipping_address_final=shipping_address_final,
        billing_address_final=billing_address_final,
        cart_id=cart_id,
        total=total,
        status=status,
        is_active=is_active
    )
    order.full_clean()
    order.save()

    return order



def order_update(*,
    order_id: int,
    data
    ) -> Order:
    
    # Obtain order 
    order = order_by_id(order_id=order_id)

    valid_fields = [
        'shipping_address',
        'shipping_total',
        'billing_address',
        'shipping_address_final',
        'billing_address_final',
        'total',
        'status',
        'is_active', 
    ]

    fields = []
    for field in valid_fields:
        if field in data:
            setattr(order, field, data[field])
            fields.append(field)
    
    if fields:
        order.full_clean()
        order.save(update_fields=fields)
    
    return order


    


def product_purchase_create(
    *,
    billing_profile_id: int,
    product_id,
    refunded:bool=False
    ):

    product_purchase = ProductPurchase(
        billing_profile_id=billing_profile,
        product_id=product_id,
        refunded=refunded
    )
    product_purchase.full_clean()
    product_purchase.save()
    
    return product_purchase



def product_purchase_update(
    *,
    product_purchase_id: int,
    data
    ) -> ProductPurchase:

    valid_fields = [
        'product_id',
        'refunded'
    ]

    # Obtain product purchase id
    product_purchase = product_purchase_by_id(product_purchase_id=product_purchase_id)
    
    fields = []
    for field in fields:
        if field in data:
            setattr(product_purchase, field, data[field])
            fields.append(field)
    
    product_purchase.full_clean()
    product_purchase.save(update_fields=fields)

    return product_purchase


    
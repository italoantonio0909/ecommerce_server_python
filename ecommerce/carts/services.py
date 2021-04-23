from django.core.exceptions import ValidationError
from ecommerce.billing.selectors import billing_profile_by_user_id
from ecommerce.billing.services import billing_profile_create
from ecommerce.orders.services import order_create
from ecommerce.products.models import Product
from ecommerce.products.selectors import product_by_id

from .models import Cart
from .selectors import cart_by_user_id, cart_get, cart_product_all


def cart_create(
    *,
    user_id: int
) -> Cart:

    cart = Cart(user_id=user_id)
    cart.full_clean()
    cart.save()

    return cart


def cart_product_add(
    *,
    product_id: int,
    cart_id: int,
    user_id: int
) -> Cart:

    product = product_by_id(product_id=product_id)

    # Obtain cart and add product
    cart = cart_get(cart_id=cart_id, user_id=user_id)

    # Check if product is in cart
    if product in cart_product_all(cart_id=cart.id):
        raise ValidationError('This product already exists in a you cart.')

    cart.products.add(product)

    return cart


def cart_product_create(
    *,
    user_id: int,
    product_id: int
) -> Cart:

    # Check user have a cart
    cart = cart_by_user_id(user_id=user_id)

    if cart:
        # If the cart exist, the product will be added
        cart_product_add(
            product_id=product_id,
            cart_id=cart.id,
            user_id=user_id
        )

    if cart is None:
        # If the cart does not exist, create cart and a product will be added
        cart = cart_create(user_id=user_id)
        cart_product_add(
            product_id=product_id,
            cart_id=cart.id,
            user_id=user_id
        )

    return cart


def cart_product_delete(
    *,
    user_id: int,
    product_id: int,
    cart_id: int
) -> Cart:

    # Obtain cart, if no exists trigger ValidationError
    cart = cart_get(cart_id=cart_id, user_id=user_id)

    # Obtain product to remove
    product = product_by_id(product_id=product_id)

    # Check product in cart
    if product not in cart_product_all(cart_id=cart.id):
        raise ValidationError('Product not exists in the cart.')

    cart.products.remove(product)

    return cart


def cart_checkout(
    *,
    cart_id: int,
    user_id: int,
) -> Cart:

    # Obtain billing profile user, if no exists return None
    billing = billing_profile_by_user_id(user_id=user_id)

    if billing is None:
        billing = billing_profile_create(user_id=user_id)

    order = order_create(
        shipping_total=0.00,
        billing_profile_id=billing.id,
        shipping_address_id=None,
        billing_address_id=None,
        shipping_address_final=None,
        billing_address_final=None,
        cart_id=cart_id,
        total=0.00,
        status='created',
        is_active=True
    )

    return order

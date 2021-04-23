from django.core.exceptions import ValidationError
from typing import Iterable
from .filters import (
    CartFilter
)

from .models import (
    Cart
)


def cart_get(*, cart_id: int, user_id: int) -> Cart:
    try:

        return Cart.objects.get(id=cart_id, user_id=user_id, is_active=True)

    except Cart.DoesNotExist:
        raise ValidationError('This cart no souch found')


def cart_by_user_id(*, user_id: int) -> Iterable[Cart]:
    try:

        return Cart.objects.get(user_id=user_id, is_active=True)

    except Cart.DoesNotExist:
        pass


def cart_product_all(*, cart_id):
    try:

        return Cart.objects.get(id=cart_id).products.all()

    except Cart.DoesNotExist:
        pass


def cart_list(*, filters=None):
    filters = filters or {}

    qs = Cart.objects.all()

    return CartFilter(filters, qs).qs

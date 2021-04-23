from django.core.exceptions import ValidationError

from .filters import OrderFilter
from .models import Order, ProductPurchase


def order_list(*, filters=None):
    filters = filters or {}

    qs = Order.objects.all()

    return OrderFilter(filters, qs).qs


def order_by_id(*, order_id: int):
    try:

        return Order.objects.get(id=order_id)

    except Order.DoesNotExist:
        raise ValidationError('This order no souch found.')


def product_purchase_by_id(*, product_purchase_id: int):
    try:

        return ProductPurchase.objects.get(id=product_purchase_id)

    except ProductPurchase.DoesNotExist:
        raise ('This product purchase no souch found.')

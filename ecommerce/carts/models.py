from django.db import models
from django.db.models.signals import (
    m2m_changed,
    pre_save
)
from decimal import Decimal


from ecommerce.core.models import BaseModel
from ecommerce.users.models import BaseUser
from ecommerce.products.models import Product


class Cart(BaseModel):
    user = models.ForeignKey(BaseUser, on_delete=models.PROTECT)
    products = models.ManyToManyField(Product)
    subtotal = models.DecimalField(
        default=0.00, max_digits=100, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.email


def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
    products = instance.products.all()
    total = 0
    for product in products:
        total += product.price_discount
    if instance.subtotal != total:
        instance.subtotal = total
        instance.save()


def pre_save_cart_receiver(sender, instance, *args, **kwargs):
    if instance.subtotal > 0:
        # Tax service 1.08
        instance.total = Decimal(instance.subtotal) * Decimal(1.05)
    else:
        instance.total = 0.00


m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.products.through)
pre_save.connect(pre_save_cart_receiver, sender=Cart)

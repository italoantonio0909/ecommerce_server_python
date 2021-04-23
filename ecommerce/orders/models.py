from django.db import models
from django.db.models.signals import (
    post_save,
    pre_save
)

from ecommerce.core.models import BaseModel
from ecommerce.users.models import BaseUser
from ecommerce.carts.models import Cart
from ecommerce.addresses.models import Address
from ecommerce.billing.models import BillingProfile
from ecommerce.products.models import Product
import math

ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded'),
)

class Order(BaseModel):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.PROTECT)
    shipping_address = models.ForeignKey(Address, related_name="shipping_address", null=True, blank=True,on_delete=models.PROTECT)
    billing_address = models.ForeignKey(Address, related_name="billing_address" ,null=True, blank=True, on_delete=models.PROTECT)
    shipping_address_final = models.TextField(blank=True, null=True)
    billing_address_final = models.TextField(blank=True, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.PROTECT)
    shipping_total = models.DecimalField(default=5.99, max_digits=100, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    status = models.CharField(max_length=100, default='created', choices=ORDER_STATUS_CHOICES)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.billing_profile.user.email

    def update_total(self):
        cart_total = self.cart.total
        shipping_total = self.shipping_total
        new_total = math.fsum([cart_total, shipping_total])
        formatted_total = format(new_total, '.2f')
        self.total = formatted_total
        self.save()
        return new_total


def pre_save_create_order(sender, instance, *args, **kwargs):
    if instance.shipping_address and not instance.shipping_address_final:
        instance.shipping_address_final = instance.shipping_address.get_address()
    
    if instance.billing_address and not instance.billing_address_final:
        instance.billing_address_final = instance.shipping_address.get_address()


def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart_total = instance.total
        cart_id = instance.id
        qs = Order.objects.filter(cart__id=cart_id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()


def post_save_order(sender, instance, created, *args, **kwargs):
    if created:
        instance.update_total()


pre_save.connect(pre_save_create_order, sender=Order)
post_save.connect(post_save_cart_total, sender=Cart)
post_save.connect(post_save_order, sender=Order)


class ProductPurchase(BaseModel):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    refunded = models.BooleanField(default=False)

    def __str__(self):
        return self.product.title
        


    
    



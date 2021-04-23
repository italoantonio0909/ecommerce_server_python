from django.db import models

from ecommerce.core.models import BaseModel
from ecommerce.users.models import BaseUser


class BillingProfile(BaseModel):
    user = models.OneToOneField(BaseUser, null=True, blank=True, on_delete=models.PROTECT)
    customer_id = models.CharField(max_length=1000 ,null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user.email
        


class Card(BaseModel):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.PROTECT)
    stripe_id = models.CharField(max_length=120)
    brand = models.CharField(max_length=120, null=True, blank=True)
    country = models.CharField(max_length=20, null=True, blank=True)
    exp_month = models.IntegerField(null=True, blank=True)
    exp_year = models.IntegerField(null=True, blank=True)
    last4 = models.CharField(max_length=4, null=True, blank=True)
    default = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "{} {}".format(self.brand, self.last4)


class Charge(BaseModel):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.PROTECT)
    stripe_id = models.CharField(max_length=120)
    paid = models.BooleanField(default=False)
    refunded = models.BooleanField(default=False)
    outcome = models.TextField(null=True, blank=True)
    outcome_type = models.CharField(max_length=120, null=True, blank=True)
    seller_message = models.CharField(max_length=120, null=True, blank=True)
    risk_level = models.CharField(max_length=120, null=True, blank=True)
    
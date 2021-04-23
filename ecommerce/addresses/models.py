from django.db import models
from ecommerce.core.models import BaseModel
from ecommerce.users.models import BaseUser
from ecommerce.billing.models import BillingProfile


ADDRESS_TYPES = (
    ('billing', 'Billing address'),
    ('shipping', 'Shipping address'),
)

class Address(BaseModel):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.PROTECT)
    name = models.CharField(max_length=120, null=True, blank=True)
    nickname = models.CharField(max_length=120, null=True, blank=True)
    address_type = models.CharField(max_length=120, choices=ADDRESS_TYPES)
    address_line_1 = models.CharField(max_length=120)
    address_line_2 = models.CharField(max_length=120, null=True, blank=True)
    city = models.CharField(max_length=120)
    country = models.CharField(max_length=120, default='Ecuador')
    postal_code = models.CharField(max_length=120)
    is_active = models.CharField(max_length=120)

    def __str__(self):
        return f'{self.user.email} {self.address_line_1}'

    def get_address(self):
        return "{for_name}\n{line1}\n{line2}\n{city}\n{state}, {postal}\n{country}".format(
                for_name = self.name or "",
                line1 = self.address_line_1,
                line2 = self.address_line_2 or "",
                city = self.city,
                state = self.state,
                postal= self.postal_code,
                country = self.country
        )
    

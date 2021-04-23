from django.contrib import admin

from .models import (
    BillingProfile,
    Charge,
    Card
)

admin.site.register(BillingProfile)
admin.site.register(Charge)
admin.site.register(Card)


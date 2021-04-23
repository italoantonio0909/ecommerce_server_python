from .models import Address
from django.core.exceptions import ValidationError

from .filters import (
    AddressFilter
)


def address_by_id(*, address_id: int):
    try:

        return Address.objects.get(id=address_id)

    except Address.DoesNotExist:
        raise ValidationError('Address no souch found.')



def address_list(*, filters=None):
    filters = filters or {}

    qs = Address.objects.all()

    return AddressFilter(filters, qs).qs
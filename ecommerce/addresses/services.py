from django.core.exceptions import ValidationError

from .models import Address
from .selectors import (
    address_by_id
)

def address_create(
    *,
        name: str,
        nickname: str,
        address_type: str,
        address_line_1: str,
        address_line_2: str,
        city: str,
        country: str,
        postal_code: str,
        is_active: bool = True
    ) -> Address:

    address = Address(
        name=name,
        nickname=nickname,
        address_type=address_type,
        address_line_1=address_line_1,
        address_line_2=address_line_2,
        city=city,
        country=country,
        postal_code=postal_code,
        is_active=is_active
    )
    address.full_clean()
    address.save()

    return address
    


def address_update(
    *,
    address_id: int,
    data,
    ) -> Address:

    valid_fields = [
        'name',
        'nickname',
        'address_type',
        'address_line_1',
        'address_line_2',
        'city',
        'country',
        'postal_code',
        'is_active'
    ]
    # Obtain address with parameter id
    address = address_by_id(address_id=address_id)
    
    fields = []
    for field in valid_fields:
        if field in data:
            setattr(address, field, data[field])
            fields.append(field)
    
    address.full_clean()
    address.save(update_fields=fields)

    return address

    

    



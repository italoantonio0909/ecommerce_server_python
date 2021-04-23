from django.core.exceptions import ValidationError

from .models import (
    BillingProfile,
    Charge,
    Card
)



def billing_profile_by_id(billing_profile_id: int) -> BillingProfile:
    try:

        return BillingProfile.objects.get(id=billing_profile_id)

    except BillingProfile.DoesNotExist:
        raise ValidationError('This billing profile no souch found.')
        

def billing_profile_by_user_id(*, user_id: int):
    try:
        
        return BillingProfile.objects.get(user_id=user_id)

    except BillingProfile.DoesNotExist:
        pass


def charge_by_id(charge_id: int) -> Charge:
    try:

        return Charge.objects.get(id=charge_id)

    except Charge.DoesNotExist:
        raise ValidationError('This charge no souch found.')
        


def card_by_id(card_id: int) -> Card:
    try:

        return Card.objects.get(id=card_id)

    except Card.DoesNotExist:
        raise ValidationError('This card no souch found.')
        

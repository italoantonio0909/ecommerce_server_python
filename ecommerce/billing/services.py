from .models import BillingProfile, Card, Charge
from .selectors import billing_profile_by_id, card_by_id, charge_by_id


def billing_profile_create(
    *,
    user_id: int,
) -> BillingProfile:

    billing = BillingProfile(user_id=user_id, customer_id=None)
    billing.full_clean()
    billing.save()

    return billing


def billing_profile_update(
    *,
    billing_profile_id: int,
    data
) -> BillingProfile:

    valid_fields = [
        'customer_id',
        'is_active',
    ]

    # Obtaing billing profile
    billing_profile = billing_profile_by_id(
        billing_profile_id=billing_profile_id)

    fields = []
    for field in valid_fields:
        if field in data:
            setattr(billing_profile, field, data[field])
            fields.append(field)

    if fields:
        billing_profile.full_clean()
        billing_profile.save(update_fields=fields)

    return billing_profile


def charge_create(
    *,
    billing_profile_id: int,
    stripe_id: str,
    paid: bool,
    refunded: bool,
    outcome: str,
    outcome_type: str = None,
    seller_message: str = None,
    risk_level: str = None
) -> Charge:

    charge = Charge(
        billing_profile_id=billing_profile_id,
        stripe_id=stripe_id,
        paid=paid,
        refunded=refunded,
        outcome=outcome,
        outcome_type=outcome_type,
        seller_message=seller_message,
        risk_level=risk_level
    )
    charge.full_clean()
    charge.save()

    return charge


def charge_update(
    *,
    charge_id: int,
    data
) -> Charge:

    valid_fields = [
        'stripe_id',
        'paid',
        'refunded',
        'outcome',
        'outcome_type',
        'seller_message',
        'risk_level'
    ]
    charge = charge_by_id(charge_id=charge_id)

    fields = []
    for field in valid_fields:
        if field in data:
            setattr(charge, field, data[field])
            fields.append(field)

    charge.full_clean()
    charge.save(update_fields=fields)

    return charge


def card_create(
    *,
    billing_profile_id: int,
    stripe_id: str,
    brand: str,
    country: str,
    exp_month: int,
    exp_year: int,
    last4: int,
    default: bool = True,
    is_active: bool = True
) -> Card:

    card = Card(
        billing_profile_id=billing_profile_id,
        stripe_id=stripe_id,
        brand=brand,
        country=country,
        exp_month=exp_month,
        exp_year=exp_year,
        last4=last4,
        default=default,
        is_active=i
    )
    card.full_clean()
    card.save()

    return card


def card_update(
    *,
    card_id: int,
    data
) -> Card:

    valid_fields = [
        'stripe_id',
        'brand',
        'country',
        'exp_month',
        'exp_year',
        'last4',
        'default',
        'is_active',
    ]

    card = card_by_id(card_id=card_id)

    fields = []
    for field in valid_fields:
        if field in data:
            setattr(card, field, data[field])
            fields.append(field)

    card.full_clean()
    card.save(update_fields=fields)

    return card

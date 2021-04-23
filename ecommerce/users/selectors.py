from django.core.exceptions import ValidationError

from .models import BaseUser
from .filters import BaseUserFilter


def user_get(*, user: BaseUser):
    return {
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'last_login': user.last_login,
        'is_active': user.is_active,
        'is_admin': user.is_admin,
        'is_superuser': user.is_superuser,
    }


def user_by_id(*, user_id: int) -> BaseUser:
    try:

        return BaseUser.objects.get(id=user_id)

    except BaseUser.DoesNotExist:
        raise ValidationError({'user': 'This user no souch found'})


def user_by_email(*, email: str) -> BaseUser:
    try:

        return BaseUser.objects.get(email=email)

    except BaseUser.DoesNotExist:
        raise ValidationError({'email': 'This email no account active'})


def user_list(*, filters=None):
    filters = filters or {}

    qs = BaseUser.objects.all()

    return BaseUserFilter(filters, qs).qs

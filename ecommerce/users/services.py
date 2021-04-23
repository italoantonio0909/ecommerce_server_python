from subprocess import call
from typing import Optional

import django.contrib.auth.password_validation as validators
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.utils.encoding import (DjangoUnicodeDecodeError, force_str,
                                   smart_bytes, smart_str)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from ecommerce.notification.services import notification_send_mail

from .events import (user_create_notify, user_password_change_notify,
                     user_password_reset_check_notify,
                     user_password_reset_notify, user_update_profile_notify)
from .models import BaseUser
from .selectors import user_by_email, user_by_id
from .utils import validate_password


def user_create(
    *,
    first_name: str,
    last_name: str,
    email: str,
    is_active: bool = True,
    is_admin: bool = False,
    password: Optional[str] = None
) -> BaseUser:

    user = BaseUser.objects.create_user(
        first_name=first_name,
        last_name=last_name,
        email=email,
        is_active=is_active,
        is_admin=is_admin,
        password=password
    )

    # Send notification create account
    user_create_notify(user_id=user.id)

    return user


def user_password_change(
    *,
    user_id: int,
    password1: str,
    password2: str,
    old_password: str
) -> BaseUser:

    user = user_by_id(user_id=user_id)

    # Password match
    if password1 != password2:
        raise ValidationError({'password': 'Password fields didn t match'})

    # Old password correct
    if not user.check_password(old_password):
        raise ValidationError({'password': 'Old password incorrect.'})

    validate_password(password=password1, username=user.email)

    user.set_password(password1)
    user.full_clean()
    user.save(update_fields=['password'])

    # Notify
    user_password_change_notify(user_id=user.id)

    return user


def user_update_profile(
    *,
    user_session,
    user_id: int,
    data
) -> BaseUser:

    # Validate if the user sent as a parameter has a
    # relationship with the user in session extracted from the token
    if user_session != user_id:
        raise ValidationError('You dont have permissions for this user.')

    # Obtain user
    user = user_by_id(user_id=user_id)

    # Valid fields optionals in parameters
    valid_fields = [
        'first_name',
        'last_name',
        'email'
    ]

    fields = []
    for field in valid_fields:
        if field in data:
            setattr(user, field, data[field])
            fields.append(field)

    if fields:
        user.full_clean()
        user.save(update_fields=fields)

        # Notify profile updated
        user_update_profile_notify(user_id=user.id)

    return user


def user_password_reset(
    *,
    email: str
) -> BaseUser:

    user, token = user_make_token(email=email)

    # Send email with credentials token
    user_password_reset_notify(user_id=user.id, token=token)

    return user, token


def user_password_reset_check(
    *,
    token: str,
    password: str
):

    try:
        # Extrack token user
        token_user = user_extract_token(token=token)

        # Extrack uidbd user id
        uidb64 = user_extract_uidb64(token=token)

        user_id = force_str(urlsafe_base64_decode(uidb64))
        user = user_by_id(user_id=user_id)

        if not PasswordResetTokenGenerator().check_token(user, token_user):
            raise ValidationError('Código no válido.')

        # Validate password strong and save a new password.
        validate_password(password=password, username=user.email)
        user.set_password(password)
        user.save(update_fields=['password'])

        # Notify success password reset
        user_password_reset_check_notify(user_id=user.id)

        return user

    except DjangoUnicodeDecodeError as e:
        raise ValidationError('Código no válido.')


def user_extract_token(*, token: str):
    separator = '_'
    try:
        # remove blank token
        token_strip = token.strip()

        # Find separator
        extract_token = token_strip.find(separator)
        if extract_token != -1:
            token_user = token[:extract_token]
        else:
            raise ValidationError('Código no válido.')

        return token_user

    except Exception:
        raise ValidationError('Código no válido.')


def user_extract_uidb64(*, token: str):
    separator = '_'
    try:
        # remove blank token
        token_strip = token.strip()

        # Find separator
        extract_uidb64 = token_strip.find(separator)
        if extract_uidb64 != -1:
            uidb64 = token[extract_uidb64 + 1:]
        else:
            raise ValidationError('Código no válido.')

        return uidb64

    except:
        raise ValidationError('Código no válido.')


def user_make_token(
    *,
    email: str
):
    user = user_by_email(email=email)

    separator = '_'
    uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
    token = PasswordResetTokenGenerator().make_token(user)
    token_formatter = f'{token}{separator}{uidb64}'

    return user, token_formatter

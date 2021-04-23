import django.contrib.auth.password_validation as validators
from django.core.exceptions import ValidationError


def validate_password(*, password: str, username:str):

    errors = dict()
    
    try:
        # Validate the password and username and catch the exception
        validators.validate_password(password=password, user=username)

    except Exception as error:
        errors['password'] = list(error.messages)
    
    if errors:
        raise ValidationError(errors)

    return password



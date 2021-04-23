from django.contrib.auth.models import BaseUserManager as BUM
from django.db import models

from .utils import validate_password


class BaseUserManager(BUM):
    

    def create_user(
        self,
        first_name,
        last_name,
        email,
        is_active=True,
        is_admin=False,
        password=None,
        ):

        if not email:
            raise ValueError('Users must have an email address')
        
        user = self.model(
            first_name=first_name.title(),
            last_name=last_name.title(),
            email=self.normalize_email(email.lower()),
            is_active=is_active,
            is_admin=is_admin
        )
        if password is not None:
            validate_password(password=password, username=email)
            user.set_password(password)
        else:
            user.set_unusable_password()
        
        user.full_clean()
        user.save(using=self._db)
        
        return user

    
    def create_superuser(
        self,
        first_name: str,
        last_name: str,
        email: str,
        password: str
        ):

        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            is_active=True,
            is_admin=True
        )

        user.is_superuser = True
        user.save(using=self._db)

        return user

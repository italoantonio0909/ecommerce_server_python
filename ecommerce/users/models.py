from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin
)

from ecommerce.core.models import BaseModel
from .managers import (
    BaseUserManager
)



class BaseUser(BaseModel, AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    # Field to validate sesion
    USERNAME_FIELD = 'email'

    # USERNAME_FIELD and password are required by default
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    # Objects manager
    objects = BaseUserManager()
    
    def __str__(self):
        return self.email

    def is_staff(self):
        return self.is_admin
    


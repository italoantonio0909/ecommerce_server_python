from django.db import models
from ecommerce.core.models import BaseModel


class Category(BaseModel):
    title = models.CharField(max_length=120, unique=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title


class Product(BaseModel):
    title = models.CharField(max_length=500,unique=True)
    description = models.CharField(max_length=1000)
    price = models.DecimalField(decimal_places=2, max_digits=100, default=39.99)
    price_discount = models.DecimalField(decimal_places=2, max_digits=100, blank=True)
    category = models.ForeignKey(Category,on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.id} {self.title}'
    
    class Meta:
        ordering=('created_at',)

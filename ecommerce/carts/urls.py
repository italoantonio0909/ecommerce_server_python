from django.urls import path, include

from .apis import (
    CartProductCreateApi,
    CartProductDeleteApi,
    CartListApi,
    CartCheckoutApi
)

carts_patterns = [
    path('create/', CartProductCreateApi.as_view(), name='create'),
    path('delete/', CartProductDeleteApi.as_view(), name='delete'),
    path('list/', CartListApi.as_view(), name='list'),
    path('checkout/', CartCheckoutApi.as_view(), name='checkout'),
]

urlpatterns = [
    path('carts/', include((carts_patterns, 'carts')))
]

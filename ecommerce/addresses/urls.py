from django.urls import path,include

from .apis import (
   AddressCreateApi,
   AddressUpdateApi,
   AddressListApi
)

addresses_patterns = [
    path('list/',AddressListApi.as_view(),name='list'),
    path('create/', AddressCreateApi.as_view(), name='create'),
    path('update/<int:address_id>/', AddressUpdateApi.as_view(), name='update'),
]

urlpatterns = [
    path('addresses/', include((addresses_patterns, 'addresses'))),
]
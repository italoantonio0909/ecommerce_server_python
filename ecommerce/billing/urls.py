from django.urls import path, include

from .apis import (
     BillingProfileCreateApi,
     BillingProfileUpdateApi,
     ChargeCreateApi,
     ChargeUpdateApi,
     CardCreateApi,
     CardUpdateApi
)

billing_profile_patterns = [
     path('create/', BillingProfileCreateApi.as_view(), name='create'),
     path('update/<int:billing_profile_id>/', BillingProfileUpdateApi.as_view(), name='update'),
]

charge_patterns = [
     path('create/', ChargeCreateApi.as_view(), name='create'),
     path('update/<int:charge_id>/', ChargeUpdateApi.as_view(), name='update')

]

cards_patterns = [
     path('create/', CardCreateApi.as_view(), name='create'),
     path('update/<int:card_id>/', CardUpdateApi.as_view(), name='update')
]

urlpatterns = [
     path('billing_profile/', include((billing_profile_patterns, 'billing_profile'))),
     path('charges/', include((charge_patterns, 'charges'))),
     path('cards/',include((cards_patterns,'cards')))
]
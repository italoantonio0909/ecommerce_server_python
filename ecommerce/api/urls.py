from django.urls import path, include

urlpatterns = [
    path('', include('ecommerce.authentication.urls')),
    path('', include('ecommerce.users.urls')),
    path('', include('ecommerce.products.urls')),
    path('', include('ecommerce.carts.urls')),
    path('', include('ecommerce.orders.urls')),
    path('', include('ecommerce.addresses.urls')),
    path('',include('ecommerce.billing.urls')),
]
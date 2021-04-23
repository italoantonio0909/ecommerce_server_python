from django.urls import include, path

from .apis import (OrderCreateApi, OrderListApi, OrderUpdateApi,
                   ProductPurchaseCreateApi, ProductPurchaseUpdateApi)

orders_patterns = [
    path('create/', OrderCreateApi.as_view(), name='create'),
    path('list/', OrderListApi.as_view(), name='list'),
    path('update/<int:order_id>/', OrderUpdateApi.as_view(), name='update')
]

products_purchases_patterns = [
    path('create/', ProductPurchaseCreateApi.as_view(), name='create'),
    path('update/', ProductPurchaseUpdateApi.as_view(), name='update')
]

urlpatterns = [
    path('orders/', include((orders_patterns, 'orders'))),
    path('products_purchases/',include((products_purchases_patterns,'products_purchases')))
]

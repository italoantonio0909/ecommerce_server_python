from django.urls import path,include

from .apis import (
    ProductListApi,
    ProductCreateApi,
    ProductUpdateApi,
    CategoryCreateApi,
    CategoryListApi,
    CategoryUpdateApi
)

product_patterns = [
    path('create/', ProductCreateApi.as_view(), name='create'),
    path('list/', ProductListApi.as_view(), name='list'),
    path('update/<int:product_id>/', ProductUpdateApi.as_view(), name='update'),
]

categories_patterns = [
    path('list/',CategoryListApi.as_view(),name='list'),
    path('create/', CategoryCreateApi.as_view(), name='create'),
    path('update/<int:category_id>/', CategoryUpdateApi.as_view(), name='update'),
]

urlpatterns = [
    path('products/', include((product_patterns, 'products'))),
    path('categories/', include((categories_patterns, 'categories')))
]
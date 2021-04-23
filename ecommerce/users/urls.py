from django.urls import path,include

from .apis import UserListApi


users_patterns = [
    path('', UserListApi.as_view(), name='list')
]

urlpatterns = [
   path('users/', include((users_patterns, 'users'))),
]
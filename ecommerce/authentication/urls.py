from django.urls import path,include

from .apis import (
    UserLoginApi,
    UserMeApi,
    UserRegisterApi,
    UserLogoutApi,
    UserPassworChangeApi,
    UserUpdateProfileApi,
    UserPasswordResetApi,
    UserPasswordResetCheckApi
)

user_patterns = [
    path('login/', UserLoginApi.as_view(), name='login'),
    path('logout/', UserLogoutApi.as_view(), name='logout'),
    path('register/',UserRegisterApi.as_view(),name='register'),
    path('me/', UserMeApi.as_view(), name='me'),
    path('password_change/<int:user_id>/', UserPassworChangeApi.as_view(), name='password_change'),
    path('update_profile/<int:user_id>/', UserUpdateProfileApi.as_view(), name='update_profile'),
    path('password_reset/', UserPasswordResetApi.as_view(), name='password_reset'),
    path('password_reset_check/<str:token>/', UserPasswordResetCheckApi.as_view(), name='password_reset_check')
]

urlpatterns = [
    path('auth/', include((user_patterns, 'auth'))),
]
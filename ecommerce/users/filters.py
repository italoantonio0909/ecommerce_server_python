import django_filters

from .models import BaseUser


class BaseUserFilter(django_filters.FilterSet):
    class Meta:
        model = BaseUser
        fields = (
            'id',
            'email',
            'is_admin',
            'first_name',
            'last_name',
            'last_login',
            'is_active'
        )

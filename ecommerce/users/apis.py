from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response

from ecommerce.api.mixins import ApiErrorsMixin

from .selectors import user_list
from .models import BaseUser


class UserListApi(ApiErrorsMixin, APIView):

    class FilterSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=False)
        is_admin = serializers.NullBooleanField(required=False)
        email = serializers.EmailField(required=False)
        first_name = serializers.CharField(required=False)
        last_name = serializers.CharField(required=False)
        last_login = serializers.DateTimeField(required=False)
        is_active = serializers.BooleanField(required=False, default=True)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = BaseUser
            fields = (
                'id',
                'first_name',
                'last_name',
                'email',
                'created_at',
                'updated_at',
                'last_login',
                'is_active',
                'is_superuser',
            )

    def get(self, request):

        # Filter querysets and validate
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        # Get users
        users = user_list(filters=filters_serializer.validated_data)

        # Dispatch format json
        data = self.OutputSerializer(users, many=True).data

        return Response(data)

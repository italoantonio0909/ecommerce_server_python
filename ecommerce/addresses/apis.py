from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response

from .services import (
    address_create,
    address_update
)
from .selectors import (
    address_list
)

from ecommerce.api.mixins import (
    ApiErrorsMixin
)
from ecommerce.core.utils import (
    inline_serializer
)



class AddressCreateApi(APIView, ApiErrorsMixin):
    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(required=False, default=None)
        nickname = serializers.CharField(required=False,default=None)
        address_type = serializers.CharField()
        address_line_1 = serializers.CharField()
        address_line_2 = serializers.CharField(required=False, default=None)
        city = serializers.CharField()
        country = serializers.CharField()
        postal_code = serializers.CharField()
        
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        address_create(**serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)



class AddressUpdateApi(APIView, ApiErrorsMixin):
    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(required=False)
        nickname = serializers.CharField(required=False)
        address_type = serializers.CharField(required=False)
        address_line_1 = serializers.CharField(required=False)
        address_line_2 = serializers.CharField(required=False)
        city = serializers.CharField(required=False)
        country = serializers.CharField(required=False)
        postal_code = serializers.CharField(required=False)

    def post(self, request, address_id):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        address_update(
            address_id=address_id,
            data=serializer.validated_data
        )

        return Response(status=status.HTTP_201_CREATED)




class AddressListApi(APIView, ApiErrorsMixin):
    class FilterSerializer(serializers.Serializer):
        postal_code = serializers.CharField(required=False)
        address_type = serializers.CharField(required=False)
        city = serializers.CharField(required=False)
        country = serializers.CharField(required=False)
        is_active = serializers.BooleanField(default=True, required=False)

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        nickname = serializers.CharField()
        address_type = serializers.CharField()
        postal_code = serializers.CharField()
        address_line_1 = serializers.CharField()
        address_line_2 = serializers.CharField()
        city = serializers.CharField()
        country = serializers.CharField()


    def get(self, request):
        filter_serializer = self.FilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)

        data = address_list(filters=filter_serializer.validated_data)
        
        address = self.OutputSerializer(data, many=True).data
        
        return Response(address)

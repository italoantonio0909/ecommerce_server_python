from ecommerce.api.mixins import ApiAuthMixin, ApiErrorsMixin
from ecommerce.core.utils import inline_serializer
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Cart
from .selectors import cart_list
from .services import cart_checkout, cart_product_create, cart_product_delete


class CartProductCreateApi(ApiAuthMixin, ApiErrorsMixin, APIView):
    class InputSerializer(serializers.Serializer):
        user_id = serializers.IntegerField()
        product_id = serializers.IntegerField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart_product_create(**serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)            



class CartProductDeleteApi(ApiAuthMixin, ApiErrorsMixin, APIView):
    class InputSerializer(serializers.Serializer):
        cart_id = serializers.IntegerField()
        user_id = serializers.IntegerField()
        product_id = serializers.IntegerField()
        
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart_product_delete(**serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)



class CartListApi(APIView, ApiErrorsMixin):
    class FilterSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=False)
        user = serializers.IntegerField(required=False)
        is_active = serializers.BooleanField(required=False,default=True)
        
    class OutputSerializer(serializers.Serializer):
        products = inline_serializer(many=True, fields={
            'id': serializers.IntegerField(),
            'title': serializers.CharField(),
            'category': serializers.CharField()
        })
        user = inline_serializer(fields={
            'id':serializers.IntegerField(),
            'email':serializers.EmailField()
        })
        subtotal = serializers.DecimalField(max_digits=100, decimal_places=2)
        total = serializers.DecimalField(max_digits=100, decimal_places=2)
        is_active = serializers.BooleanField()
    
    def get(self, request):
        filter_serializer = self.FilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)

        carts = cart_list(filters=filter_serializer.validated_data)
        
        data = self.OutputSerializer(carts, many=True).data
        
        return Response(data)



class CartCheckoutApi(APIView, ApiErrorsMixin):
    class InputSerializer(serializers.Serializer):
        cart_id = serializers.IntegerField()
        user_id = serializers.IntegerField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart_checkout(**serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)

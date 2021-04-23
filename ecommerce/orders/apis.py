from ecommerce.api.mixins import ApiErrorsMixin
from ecommerce.core.utils import inline_serializer
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .selectors import order_list
from .services import (order_create, order_update, product_purchase_create,
                       product_purchase_update)


class OrderListApi(APIView):
    class FilterSerializer(serializers.Serializer):
        cart = serializers.IntegerField(required=False)
        is_active = serializers.BooleanField(default=True, required=False)
        status = serializers.CharField(required=False)
    
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        cart = inline_serializer(fields={
            'id': serializers.IntegerField(),
            'subtotal':serializers.DecimalField(default=0.00, max_digits=100, decimal_places=2),
            'total':serializers.DecimalField(default=0.00, max_digits=100, decimal_places=2)
        })
        total = serializers.DecimalField(default=0.00, max_digits=100, decimal_places=2)
        status = serializers.CharField()
        is_active = serializers.BooleanField()
        
    
    def get(self, request):
        filter_serializer = self.FilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)

        orders = order_list(filters=filter_serializer.validated_data)
        
        data = self.OutputSerializer(orders, many=True).data
        
        return Response(data)
        


class OrderCreateApi(APIView):
    class InputSerializer(serializers.Serializer):
        billing_profile_id = serializers.IntegerField() 
        shipping_address_id = serializers.IntegerField()
        billing_address_id = serializers.IntegerField()
        shipping_address_final = serializers.CharField(required=False)
        billing_address_final = serializers.CharField(required=False)
        cart_id = serializers.IntegerField()
        total = serializers.DecimalField(default=0.00, required=False, decimal_places=2, max_digits=100)
        status = serializers.CharField(required=False)
        is_active = serializers.BooleanField(required=False)
    
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order_create(**serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)



class OrderUpdateApi(APIView, ApiErrorsMixin):
    class InputSerializer(serializers.Serializer):
        shipping_address = serializers.IntegerField(required=False)
        billing_address = serializers.IntegerField(required=False)
        shipping_address_final = serializers.CharField(required=False)
        billing_address_final = serializers.CharField(required=False)
        total = serializers.DecimalField(required=False, decimal_places=2, max_digits=100)
        status = serializers.CharField(required=False)
        is_active = serializers.BooleanField(required=False)
    
    def post(self, request, order_id):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order_update(order_id=order_id, data=serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)

    

class ProductPurchaseCreateApi(APIView, ApiErrorsMixin):
    class InputSerializer(serializers.Serializer):
        billing_profile_id = serializers.IntegerField()
        product_id = serializers.IntegerField()
        refunded = serializers.BooleanField(required=False, default=False)

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_purchase_create(**serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)

    

class ProductPurchaseUpdateApi(APIView, ApiErrorsMixin):
    class InputSerializer(serializers.Serializer):
        product_id = serializers.IntegerField(required=False)
        refunded = serializers.CharField(required=False)

    def post(self, request, product_purchase_id):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_purchase_update(product_purchase_id=product_purchase_id,
            data=serializer.validated_data
        )

        return Response(status=status.HTTP_201_CREATED)

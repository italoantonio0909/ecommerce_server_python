from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from rest_framework.views import APIView

from ecommerce.api.mixins import ApiAuthMixin, ApiErrorsMixin

from .services import (
    billing_profile_create,
    billing_profile_update,
    charge_create,
    charge_update,
    card_create,
    card_update
)



class BillingProfileCreateApi(APIView, ApiErrorsMixin):
    class InputSerializer(serializers.Serializer):
        user_id = serializers.IntegerField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        billing_profile_create()

        return Response(status=status.HTTP_201_CREATED)



class BillingProfileUpdateApi(APIView, ApiErrorsMixin):
    class InputSerializer(serializers.Serializer):
        customer_id = serializers.CharField(required=False)
        is_active = serializers.BooleanField(required=False)
        
    def post(self, request, billing_profile_id):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        billing_profile_update(
            billing_profile_id=billing_profile_id,
            data=serializer.validated_data
        )
        
        return Response(status=status.HTTP_201_CREATED)


class ChargeCreateApi(APIView, ApiErrorsMixin):
    class InputSerializer(serializers.Serializer):
        billing_profile_id = serializers.IntegerField()
        stripe_id = serializers.CharField()
        paid = serializers.BooleanField(required=False, default=False)
        refunded = serializers.BooleanField(required=False, default=False)
        outcome = serializers.CharField()
        outcome_type = serializers.CharField(required=False,default=None)
        seller_message = serializers.CharField(required=False,default=None)
        risk_level = serializers.CharField(required=False,default=None)

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        charge_create(**serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)



class ChargeUpdateApi(APIView, ApiErrorsMixin):
    class InputSerializer(serializers.Serializer):
        stripe_id = serializers.CharField(required=False)
        paid = serializers.BooleanField(required=False)
        refunded = serializers.BooleanField(required=False)
        outcome = serializers.CharField(required=False)
        outcome_type = serializers.CharField(required=False)
        seller_message = serializers.CharField(required=False)
        risk_level = serializers.CharField(required=False)
    
    def post(self, request, charge_id):
        serializer = self.InputSerializer(data=request.data).data
        serializer.is_valid(raise_exception=True)

        charge_update(charge_id=charge_id, data=serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)




class CardCreateApi(APIView, ApiErrorsMixin):
    class InputSerializer(serializers.Serializer):
        billing_profile_id = serializers.IntegerField()
        stripe_id = serializers.CharField()
        brand = serializers.CharField(required=False, default=None)
        country = serializers.CharField(required=False, default=None)
        exp_month = serializers.IntegerField(required=False, default=0)
        exp_year = serializers.IntegerField(required=False, default=0)
        last4 = serializers.CharField(default=None, required=None)
        default = serializers.BooleanField()
        is_active = serializers.BooleanField(required=False, default=True)

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        card_create(**serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)



class CardUpdateApi(APIView, ApiErrorsMixin):
    class InputSerializer(serializers.Serializer):
        stripe_id = serializers.CharField(required=False)
        brand = serializers.CharField(required=False)
        country = serializers.CharField(required=False)
        exp_month = serializers.IntegerField(required=False)
        exp_year = serializers.IntegerField(required=False)
        last4 = serializers.CharField(default=None)
        default = serializers.BooleanField(required=False)
        is_active = serializers.BooleanField(required=False)

    def post(self, request, card_id):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        card_update(card_id=card_id, data=serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)

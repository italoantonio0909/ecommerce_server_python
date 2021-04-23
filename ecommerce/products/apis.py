from ecommerce.api.mixins import ApiAuthMixin, ApiErrorsMixin
from ecommerce.core.utils import inline_serializer
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, Product
from .selectors import category_list, product_list
from .services import (category_create, category_update, product_create,
                       product_update)


class ProductListApi(ApiAuthMixin, ApiErrorsMixin, APIView):
    """This class allows list products 
       and filter them by any parameter


    """
    class FilterSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=False)
        title = serializers.CharField(required=False)
        description = serializers.CharField(required=False)
        price = serializers.DecimalField(required=False,decimal_places=2, max_digits=20)
        price_discount = serializers.DecimalField(required=False,decimal_places=2, max_digits=20)
        category = serializers.IntegerField(required=False)
    
    class InputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        title = serializers.CharField()
        description = serializers.CharField()
        price = serializers.DecimalField(required=False, decimal_places=2, max_digits=20)
        price_discount = serializers.DecimalField(required=False, decimal_places=2, max_digits=20)
        category = inline_serializer(fields={
            'id': serializers.IntegerField(),
            'title': serializers.CharField()
        })

    def get(self, request):

        # Filter querysets and validate
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        #Get products
        products = product_list(filters=filters_serializer.validated_data)

        data = self.InputSerializer(products,many=True).data
        
        return Response(data)



class ProductCreateApi(ApiAuthMixin, ApiErrorsMixin, APIView):
    """This class allows you to create products based on a category


    Parameters:
    title -- Title of product
    description -- Product features
    price -- Price product
    price_discount -- Price optional
    category -- Id of category
    """

    class InputSerializer(serializers.Serializer):
        title = serializers.CharField()
        description = serializers.CharField()
        price = serializers.DecimalField(decimal_places=2, max_digits=20)
        price_discount = serializers.DecimalField(required=False,decimal_places=2, max_digits=20)
        category = serializers.IntegerField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        product_create(**serializer.validated_data)
        
        return Response(status=status.HTTP_201_CREATED)
        


class ProductUpdateApi(ApiAuthMixin, ApiErrorsMixin, APIView):
    """Class that allows updating data of an existing product


    Parameters:
    title -- Title of product
    description -- Product features
    price -- Price product
    price_discount -- Price optional
    category -- Id of category
    """

    class InputSerializer(serializers.Serializer):
        title = serializers.CharField(required=False)
        description = serializers.CharField(required=False)
        price = serializers.DecimalField(decimal_places=2, max_digits=20,required=False)
        price_discount = serializers.DecimalField( decimal_places=2, max_digits=20, required=False)
        category = serializers.IntegerField(required=False)
    
    def post(self, request, product_id):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        product_update(product_id=product_id, data=serializer.validated_data)
        
        return Response(status=status.HTTP_201_CREATED)        



class CategoryListApi(ApiAuthMixin, ApiErrorsMixin, APIView):
    """This class allows you to list users 
       and filter them by any parameter


    """
    class FilterSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=False)
        title = serializers.CharField(required=False)
        is_active = serializers.BooleanField(required=False)
    
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Category
            fields = (
                'id',
                'title',
                'is_active'
            )

    def get(self, request):

        # Filter querysets and validate
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        # Get categories
        categories = category_list(filters=filters_serializer.validated_data)

        data = self.OutputSerializer(categories,many=True).data
        
        return Response(data)



class CategoryCreateApi(ApiAuthMixin, ApiErrorsMixin, APIView):
    """Class that allows creating a category


    Parameters:
    title -- Name of category
    is_active -- Default true
    """
    class InputSerializer(serializers.Serializer):
        title = serializers.CharField()
        is_active = serializers.BooleanField(default=True)

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        category_create(**serializer.validated_data)
        
        return Response(status=status.HTTP_201_CREATED)        



class CategoryUpdateApi(ApiAuthMixin, ApiErrorsMixin, APIView):
    """Class that allows updating a category


    Parameters:
    title -- Name of category
    is_active -- Default true
    """
    
    class InputSerializer(serializers.Serializer):
        title = serializers.CharField()
        is_active = serializers.BooleanField(default=True)
        
    def post(self, request, category_id):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        category_update(category_id=category_id, data=serializer.validated_data)
        
        return Response(status=status.HTTP_201_CREATED)
        
from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from ecommerce.api.mixins import ApiErrorsMixin



class GenericServiceApi(GenericAPIView, ApiErrorsMixin):

    def get_service(self):
        raise NotImplemented()

    def get_response(self):
        raise NotImplemented()
    
    def transform_data(self, serializer):
        return serializer.validate_data

    def call_service(self, **validate_data):
        service = self.get_service(**validate_data)
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exceptions=True)

        data_service = self.transform_data(serializer)
        service_result = self.call_service(data_service)
        
        self.get_response(service_result)

        return response
        




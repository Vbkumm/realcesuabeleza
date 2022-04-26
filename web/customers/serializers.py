from rest_framework import serializers
from .models import (CustomerModel,
                     CustomerUserModel,
                     CustomerAddressModel,
                     CustomerPhoneModel,
                     )


class CustomerCreateSerializer(serializers.Serializer):

    class Meta:
        model = CustomerModel
        fields = ['business', 'name', 'id', 'is_active', 'birth_date', 'federal_id',  'email', 'receive_email', 'schedule_active', 'updated_at', 'updated_by', 'created_by',  'created']


class CustomerUserCreateSerializer(serializers.Serializer):

    class Meta:
        model = CustomerUserModel
        fields = ['business', 'name', 'id', 'is_active', 'birth_date', 'federal_id',  'email', 'receive_email', 'schedule_active', 'updated_at', 'updated_by', 'created_by',  'created']


class CustomerAddressCreateSerializer(serializers.Serializer):

    class Meta:
        model = CustomerAddressModel
        fields = ['customer', 'is_active', 'id', 'zip_code', 'street', 'street_number',  'district', 'city', 'state', 'updated_at', 'updated_by', 'created_by',  'created']


class CustomerPhoneCreateSerializer(serializers.Serializer):

    class Meta:
        model = CustomerPhoneModel
        fields = ['customer', 'is_active', 'id', 'phone', 'updated_at', 'updated_by', 'created_by',  'created']

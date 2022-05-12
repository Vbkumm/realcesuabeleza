from rest_framework import serializers
from .models import (CustomerModel,
                     CustomerUserModel,
                     CustomerAddressModel,
                     CustomerPhoneModel,
                     )


class CustomerUserSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = CustomerUserModel
        fields = ['business', 'name', 'id', 'is_active', 'birth_date', 'federal_id',  'email', 'receive_email', 'schedule_active', 'updated_at', 'updated_by', 'created_by',  'created']


class CustomerAddressSerializer(serializers.Serializer):
    zip_code = serializers.CharField(max_length=150)
    street = serializers.CharField(max_length=150)
    street_number = serializers.CharField(max_length=150)
    district = serializers.CharField(max_length=150)
    city = serializers.CharField(max_length=150)
    state = serializers.CharField(max_length=150)

    class Meta:
        model = CustomerAddressModel
        fields = ['customer', 'is_active', 'id', 'zip_code', 'street', 'street_number',  'district', 'city', 'state', 'updated_at', 'updated_by', 'created_by',  'created']


class CustomerPhoneSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=150)

    class Meta:
        model = CustomerPhoneModel
        fields = ['customer', 'is_active', 'id', 'phone', 'updated_at', 'updated_by', 'created_by',  'created']


class CustomerSerializer(serializers.Serializer):
    business = serializers.StringRelatedField(many=False)
    name = serializers.CharField()
    birth_date = serializers.CharField()
    federal_id = serializers.CharField()
    phones = CustomerPhoneSerializer(source='customer_phone', many=True, read_only=True)
    addresses = CustomerAddressSerializer(source='customer_address', many=True, read_only=True)
    receive_email = serializers.BooleanField()
    schedule_active = serializers.BooleanField()
    is_active = serializers.BooleanField()
    url = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta:
        model = CustomerModel
        fields = ['business', 'name', 'id', 'is_active', 'birth_date', 'federal_id',  'email', 'receive_email', 'schedule_active', 'updated_at', 'updated_by', 'created_by',  'created']


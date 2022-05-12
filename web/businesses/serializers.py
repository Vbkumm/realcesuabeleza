from rest_framework import serializers
from accounts.serializers import CustomUserSerializer
from .models import (BusinessModel,
                     BusinessAddressModel,
                     BusinessPhoneModel,)


class BusinessPhoneSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=150)

    class Meta:
        model = BusinessPhoneModel
        fields = ['address', 'id', 'is_active', 'phone', 'updated_by', 'updated_at', 'created_by', 'created',]


class BusinessAddressSerializer(serializers.Serializer):
    zip_code = serializers.CharField(max_length=150)
    street = serializers.CharField(max_length=150)
    street_number = serializers.CharField(max_length=150)
    district = serializers.CharField(max_length=150)
    city = serializers.CharField(max_length=150)
    state = serializers.CharField(max_length=150)
    phones = BusinessPhoneSerializer(source='business_address_phone', many=True, read_only=True)

    class Meta:
        model = BusinessAddressModel
        fields = ['business', 'id', 'is_active', 'zip_code', 'street',  'street_number', 'district', 'city', 'state',
                  'updated_by', 'updated_at', 'created_by', 'created',]


class BusinessSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=150)
    slug = serializers.CharField(max_length=150)
    federal_id = serializers.CharField(max_length=15,)
    description = serializers.CharField()
    owners = CustomUserSerializer(read_only=True, many=True) # serializers.SerializerMethodField(read_only=True)
    users = CustomUserSerializer(read_only=True, many=True) # serializers.SerializerMethodField(read_only=True)
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    addresses = BusinessAddressSerializer(source='business', many=True, read_only=True)

    class Meta:
        model = BusinessModel
        fields = ['id', 'title', 'slug', 'email', 'description', 'birth_date', 'federal_id', 'owners',  'users',
                  'is_active', 'updated_by', 'updated_at', 'created_by', 'created', 'url']

    # def __init__(self, *args, **kwargs):
    #      kwargs['federal_id'] = serializers.RegexField(regex='(/(^\d{3}\.\d{3}\.\d{3}\-\d{2}$)|(^\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2}$)/$)')
    #      super().__init__(*args, **kwargs)

    # def title_business_serializer(self, value):
    #     """
    #     Check that the business name is unique.
    #     """
    #     if 'django' not in value.lower():
    #         raise serializers.ValidationError("Ups erro!")
    #     return value

        # user = None
        # request = self.context.get("request")
        # if request and hasattr(request, "user"):
        #     user = request.user
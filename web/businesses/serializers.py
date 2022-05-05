from rest_framework import serializers
from accounts.serializers import PublicCustomUserSerializer
from .models import (BusinessModel,
                     BusinessAddressModel,
                     BusinessPhoneModel,)


class BusinessSerializer(serializers.Serializer):
    # title = serializers.CharField(max_length=150)
    # slug = serializers.CharField(max_length=150)
    # federal_id = serializers.CharField(max_length=15,)
    # description = serializers.CharField()
    # owners = PublicCustomUserSerializer(source='user.CustomUserModel', read_only=True) # serializers.SerializerMethodField(read_only=True)
    # birth_date = serializers.SerializerMethodField(read_only=True)
    url = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta:
        model = BusinessModel
        fields = ['id', 'title', 'slug', 'email', 'description', 'birth_date', 'federal_id', 'owners',  'users',
                  'is_active', 'updated_by', 'updated_at', 'created_by', 'created', 'url']

    # def __init__(self, *args, **kwargs):
    #     kwargs['federal_id'] = serializers.RegexField(regex='(/(^\d{3}\.\d{3}\.\d{3}\-\d{2}$)|(^\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2}$)/$)')
    #     super().__init__(*args, **kwargs)

    # def title_business_serializer(self, value):
    #     """
    #     Check that the business name is unique.
    #     """
    #     if 'django' not in value.lower():
    #         raise serializers.ValidationError("Ups erro!")
    #     return value


class BusinessAddressSerializer(serializers.Serializer):

    class Meta:
        model = BusinessAddressModel
        fields = ['business', 'id', 'is_active', 'zip_code', 'street',  'street_number', 'district', 'city', 'state',
                  'updated_by', 'updated_at', 'created_by', 'created',]


class BusinessPhoneSerializer(serializers.Serializer):

    class Meta:
        model = BusinessPhoneModel
        fields = ['address', 'id', 'is_active', 'phone', 'updated_by', 'updated_at', 'created_by', 'created',]

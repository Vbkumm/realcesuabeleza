from rest_framework import serializers
from .models import (EquipmentModel,
                     EquipmentAddressModel,
                     ServiceEquipmentModel,
                     ServiceCategoryModel,
                     ServiceModel)


class EquipmentCreateSerializer(serializers.Serializer):

    class Meta:
        model = EquipmentModel
        fields = ['business', 'title', 'id', 'slug', 'description', 'addresses', 'updated_at', 'updated_by', 'created_by',  'created']


class EquipmentAddressCreateSerializer(serializers.Serializer):

    class Meta:
        model = EquipmentAddressModel
        fields = ['address', 'equipment', 'id', 'qty', 'is_active', 'updated_at', 'updated_by', 'created_by',  'created']


class ServiceEquipmentCreateSerializer(serializers.Serializer):

    class Meta:
        model = ServiceEquipmentModel
        fields = ['service', 'equipment', 'id', 'equipment_time', 'equipment_complement', 'equipment_replaced', 'updated_at', 'updated_by', 'created_by',  'created']


class ServiceCategoryCreateSerializer(serializers.Serializer):

    class Meta:
        model = ServiceCategoryModel
        fields = ['business', 'title', 'id', 'slug', 'is_active', 'updated_at', 'updated_by', 'created_by',  'created']


class ServiceCreateSerializer(serializers.Serializer):

    class Meta:
        model = ServiceModel
        fields = ['business', 'title', 'id', 'slug', 'description', 'is_active', 'schedule_active', 'cancel_schedule_active', 'service_category', 'equipments', '_views', 'updated_at', 'updated_by', 'created_by',  'created']

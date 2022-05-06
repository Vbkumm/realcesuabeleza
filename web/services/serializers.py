from rest_framework import serializers
from .models import (EquipmentModel,
                     EquipmentAddressModel,
                     ServiceEquipmentModel,
                     ServiceCategoryModel,
                     ServiceModel)


class ServiceEquipmentSerializer(serializers.Serializer):
    equipment_time = serializers.CharField(max_length=150)
    equipment_complement = serializers.BooleanField(required=False)#se complementa algum equipamento para realizacao do servico
    equipment_replaced = serializers.StringRelatedField(many=False)#se junto com a aterior indica equipamento q ele complenta para realizar o servico, se sozinha equipamento substitui o principal

    class Meta:
        model = ServiceEquipmentModel
        fields = ['service', 'equipment', 'id', 'equipment_time', 'equipment_complement', 'equipment_replaced', 'updated_at', 'updated_by', 'created_by',  'created']


class EquipmentSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=150)
    slug = serializers.CharField(max_length=150)

    class Meta:
        model = EquipmentModel
        fields = ['business', 'title', 'id', 'slug', 'description', 'addresses', 'updated_at', 'updated_by', 'created_by',  'created']


class EquipmentAddressSerializer(serializers.Serializer):
    CHOICES = EquipmentAddressModel.CHOICES
    equipment = EquipmentSerializer(many=False)
    address = serializers.StringRelatedField(many=False)
    qty = serializers.ChoiceField(choices=CHOICES, default=1)

    class Meta:
        model = EquipmentAddressModel
        fields = ['address', 'equipment', 'id', 'qty', 'is_active', 'updated_at', 'updated_by', 'created_by',  'created']


class ServiceCategorySerializer(serializers.Serializer):
    title = serializers.CharField(max_length=150)
    slug = serializers.CharField(max_length=150)
    url = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta:
        model = ServiceCategoryModel
        fields = ['business', 'title', 'id', 'slug', 'is_active', 'updated_at', 'updated_by', 'created_by',  'created']


class ServiceSerializer(serializers.Serializer):
    business = serializers.StringRelatedField(many=False)
    service_category = ServiceCategorySerializer(many=False, read_only=True)
    title = serializers.CharField(max_length=150)
    slug = serializers.CharField(max_length=150)
    description = serializers.CharField()
    equipments = EquipmentSerializer(many=True, read_only=True,)
    url = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta:
        model = ServiceModel
        fields = ['business', 'title', 'id', 'slug', 'description', 'is_active', 'schedule_active', 'cancel_schedule_active', 'service_category', 'equipments', '_views', 'updated_at', 'updated_by', 'created_by',  'created']

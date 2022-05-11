from rest_framework import serializers
from .models import (ProfessionalModel,
                     ProfessionalCategoryModel,
                     ProfessionalPhoneModel,
                     ProfessionalUserModel,
                     ProfessionalAddressModel,
                     ProfessionalScheduleModel,
                     ProfessionalNoSkillModel,
                     ProfessionalExtraSkillModel,
                     ProfessionalServiceCategoryModel,
                     OpenScheduleModel,
                     CloseScheduleModel,
                     )
from services.serializers import ServiceCategorySerializer
from businesses.serializers import BusinessAddressSerializer


class ProfessionalServiceCategorySerializer(serializers.Serializer):
    service_category = ServiceCategorySerializer(many=False, read_only=True)

    class Meta:
        model = ProfessionalServiceCategoryModel
        fields = ['service_category', 'professional_category', 'created_by',  'created']


class ProfessionalCategorySerializer(serializers.Serializer):
    title = serializers.CharField(max_length=150)
    slug = serializers.CharField(max_length=150)
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    service_category = ProfessionalServiceCategorySerializer(source='professional_category_set', many=True)

    class Meta:
        model = ProfessionalCategoryModel
        fields = ['business', 'title', 'id', 'is_active', 'birth_date', 'service_category', 'updated_at', 'updated_by',
                  'created_by',  'created']


class ProfessionalScheduleSerializer(serializers.Serializer):
    address = serializers.StringRelatedField(many=False)
    week_days = serializers.IntegerField()
    start_hour = serializers.TimeField()
    end_hour = serializers.TimeField()

    class Meta:
        model = ProfessionalScheduleModel
        fields = ['id', 'address', 'professional', 'week_days', 'start_hour', 'end_hour', 'fraction_time',
                  'updated_at', 'updated_by', 'created_by',  'created']


class ProfessionalNoSkillSerializer(serializers.Serializer):
    service = serializers.StringRelatedField(many=False)

    class Meta:
        model = ProfessionalNoSkillModel
        fields = ['service', 'professional', 'created_by',  'created']


class ProfessionalExtraSkillSerializer(serializers.Serializer):
    service = serializers.StringRelatedField(many=False)
    
    class Meta:
        model = ProfessionalExtraSkillModel
        fields = ['service', 'professional', 'created_by',  'created']


class ProfessionalSerializer(serializers.Serializer):
    business = serializers.StringRelatedField(many=False)
    category = ProfessionalCategorySerializer(many=True, read_only=True)
    name = serializers.CharField(max_length=150)
    slug = serializers.CharField(max_length=150)
    federal_id = serializers.CharField()
    schedule_active = serializers.BooleanField()
    cancel_schedule_active = serializers.BooleanField()
    addresses = ProfessionalScheduleSerializer(source='professional_schedule', many=True)
    extra_skills = ProfessionalExtraSkillSerializer(source='professional_extra_skill_set', many=True)
    no_skills = ProfessionalNoSkillSerializer(source='professional_no_skill_set', many=True)

    url = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta:
        model = ProfessionalModel
        fields = ['business', 'began_date', 'name', 'id', 'is_active', 'birth_date', 'federal_id', 'slug',
                  'category', 'schedule_active', 'cancel_schedule_active', 'addresses', 'extra_skills',
                  'no_skills','_views', 'updated_at', 'updated_by', 'created_by',  'created']


class ProfessionalPhoneSerializer(serializers.Serializer):

    class Meta:
        model = ProfessionalPhoneModel
        fields = ['professional', 'phone', 'id', 'is_active', 'updated_at', 'updated_by', 'created_by',
                  'created']


class ProfessionalUserSerializer(serializers.Serializer):

    class Meta:
        model = ProfessionalUserModel
        fields = ['user', 'professional', 'updated_at', 'updated_by', 'created_by',  'created']


class ProfessionalAddressSerializer(serializers.Serializer):

    class Meta:
        model = ProfessionalAddressModel
        fields = ['professional', 'id', 'is_active', 'zip_code', 'street', 'street_number',
                  'district', 'city', 'state', 'updated_at', 'updated_by', 'created_by',  'created']


class OpenScheduleSerializer(serializers.Serializer):

    class Meta:
        model = OpenScheduleModel
        fields = ['id', 'business', 'address', 'start_date', 'end_date', 'start_hour', 'end_hour', 'fraction_time',
                  'professionals', 'description', 'updated_at', 'updated_by', 'created_by',  'created']


class CloseScheduleSerializer(serializers.Serializer):

    class Meta:
        model = CloseScheduleModel
        fields = ['id', 'business', 'address', 'start_date', 'end_date', 'start_hour', 'end_hour', 'fraction_time',
                  'professionals', 'description', 'updated_at', 'updated_by', 'created_by',  'created']

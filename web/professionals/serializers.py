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


class ProfessionalCreateSerializer(serializers.Serializer):

    class Meta:
        model = ProfessionalModel
        fields = ['business', 'began_date', 'name', 'id', 'is_active', 'birth_date', 'federal_id', 'slug',
                  'category', 'schedule_active', 'cancel_schedule_active', 'addresses', 'extra_skills',
                  'no_skills','_views', 'updated_at', 'updated_by', 'created_by',  'created']


class ProfessionalCategorySerializer(serializers.Serializer):

    class Meta:
        model = ProfessionalCategoryModel
        fields = ['business', 'title', 'id', 'is_active', 'birth_date', 'updated_at', 'updated_by',
                  'created_by',  'created']


class ProfessionalPhoneModelCreateSerializer(serializers.Serializer):

    class Meta:
        model = ProfessionalPhoneModel
        fields = ['professional', 'phone', 'id', 'is_active', 'updated_at', 'updated_by', 'created_by',
                  'created']


class ProfessionalUserCreateSerializer(serializers.Serializer):

    class Meta:
        model = ProfessionalUserModel
        fields = ['user', 'professional', 'updated_at', 'updated_by', 'created_by',  'created']


class ProfessionalAddressModelSerializer(serializers.Serializer):

    class Meta:
        model = ProfessionalAddressModel
        fields = ['professional', 'id', 'is_active', 'zip_code', 'street', 'street_number',
                  'district', 'city', 'state', 'updated_at', 'updated_by', 'created_by',  'created']


class ProfessionalScheduleModelCreateSerializer(serializers.Serializer):

    class Meta:
        model = ProfessionalScheduleModel
        fields = ['id', 'address', 'professional', 'week_days', 'start_hour', 'end_hour', 'fraction_time',
                  'updated_at', 'updated_by', 'created_by',  'created']


class ProfessionalNoSkillCreateSerializer(serializers.Serializer):

    class Meta:
        model = ProfessionalNoSkillModel
        fields = ['service', 'professional', 'created_by',  'created']


class ProfessionalExtraSkillCreateSerializer(serializers.Serializer):

    class Meta:
        model = ProfessionalExtraSkillModel
        fields = ['service', 'professional', 'created_by',  'created']


class ProfessionalServiceCategoryCreateSerializer(serializers.Serializer):

    class Meta:
        model = ProfessionalServiceCategoryModel
        fields = ['service_category', 'professional_category', 'created_by',  'created']


class OpenScheduleCreateSerializer(serializers.Serializer):

    class Meta:
        model = OpenScheduleModel
        fields = ['id', 'business', 'address', 'start_date', 'end_date', 'start_hour', 'end_hour', 'fraction_time',
                  'professionals', 'description', 'updated_at', 'updated_by', 'created_by',  'created']


class CloseScheduleCreateSerializer(serializers.Serializer):

    class Meta:
        model = CloseScheduleModel
        fields = ['id', 'business', 'address', 'start_date', 'end_date', 'start_hour', 'end_hour', 'fraction_time',
                  'professionals', 'description', 'updated_at', 'updated_by', 'created_by',  'created']

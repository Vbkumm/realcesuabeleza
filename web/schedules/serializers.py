from rest_framework import serializers
from .models import (ScheduleModel, ScheduleExtraTimeModel,)


class ScheduleCreateSerializer(serializers.Serializer):

    class Meta:
        model = ScheduleModel
        fields = ['id', 'address', 'service', 'customer', 'professional', 'date', 'hour', 'description',
                  '_done', '_paid', '_canceled', 'equipments_extra_time', 'updated_at', 'updated_by',
                  'created_by',  'created']


class ScheduleExtraTimeCreateSerializer(serializers.Serializer):

    class Meta:
        model = ScheduleExtraTimeModel
        fields = ['id', 'schedule', 'service_equipment', 'extra_time', 'updated_at', 'updated_by',
                  'created_by',  'created']
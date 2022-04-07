from rest_framework import serializers

from .models import CustomUserModel


class PublicCustomUserSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField(read_only=True)
    last_name = serializers.SerializerMethodField(read_only=True)
    federal_id = serializers.SerializerMethodField(read_only=True)
    email = serializers.SerializerMethodField(read_only=True)
    phone = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUserModel
        fields = [
            "first_name",
            "last_name",
            "id",
            "federal_id",
            "phone",

        ]

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name

from rest_framework import serializers

from . import services
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        return services.UserDataClass(**data)


class UserGetSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

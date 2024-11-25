from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Car

UserModel = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        return UserModel.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )

    class Meta:
        model = UserModel
        fields = ("id", "username", "password")


class CarSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Car
        fields = '__all__'

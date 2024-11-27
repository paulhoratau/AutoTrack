from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Car, CarRepair

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

class CarRepairSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = CarRepair
        fields = '__all__'


class CarSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    repairs = CarRepairSerializer(many=True, read_only=True)  # Fetch repairs using related_name

    class Meta:
        model = Car
        fields = '__all__'

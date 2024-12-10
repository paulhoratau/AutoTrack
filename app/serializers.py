from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Car, CarRepair, CarReminder, CarModel, Booking, Key, KeyHistory, Location
from .validators import validate_time_overlap

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

class CarReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarReminder
        fields = '__all__'

class CarSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    repairs = CarRepairSerializer(many=True, read_only=True)
    reminders = CarReminderSerializer(many=True, read_only=True)

    class Meta:
        model = Car
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    class Meta:
        model = Booking
        fields = '__all__'


    def validate(self, data):
        """
        Validate booking data, including overlap checks.
        """
        instance = getattr(self, 'instance', None)
        validate_time_overlap(
            start_time=data.get('start_time'),
            end_time=data.get('end_time'),
            car=data.get('car'),
            instance=instance
        )
        return data
class CarModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = '__all__'


class KeySerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    booking = serializers.PrimaryKeyRelatedField(queryset=Booking.objects.all())
    start_time = serializers.DateTimeField(source='booking.start_time', read_only=True)
    end_time = serializers.DateTimeField(source='booking.end_time', read_only=True)

    class Meta:
        model = Key
        fields = '__all__'

class KeyHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyHistory
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

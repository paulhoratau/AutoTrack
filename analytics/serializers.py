
from rest_framework import serializers
from .models import TripSummary, EventSummary


class TripSummarySerializer(serializers.ModelSerializer):

    class Meta:
        model = TripSummary
        fields = '__all__'

class EventSummarySerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user__id')
    user_email = serializers.EmailField(source='user__email')
    low_total = serializers.IntegerField()
    medium_total = serializers.IntegerField()
    high_total = serializers.IntegerField()
    overspeed_total = serializers.IntegerField()
    total_alerts = serializers.IntegerField()
    class Meta:
        model = EventSummary
        fields = '__all__'

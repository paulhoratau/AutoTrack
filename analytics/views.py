from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import EventSummary, TripSummary
from .serializers import EventSummarySerializer, TripSummarySerializer
from .utils import meters_to_miles, calculate_total, count_by_field, generate_by_time_period, get_driver_event_summary
from django.db.models import Count, Case, When, Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status



class EventViewSet(viewsets.ModelViewSet):
    queryset = EventSummary.objects.all()
    serializer_class = EventSummarySerializer
    http_method_names = ['get']
    #permission_classes = [IsAuthenticated]


class DriverEventSummaryViewSet(viewsets.ModelViewSet):
    queryset = EventSummary.objects.all()
    serializer_class = EventSummarySerializer
    http_method_names = ['get']
    #permission_classes = [IsAuthenticated]

    def get_queryset(self):
        ALERT_LOW = 'low'
        ALERT_MEDIUM = 'medium'
        ALERT_HIGH = 'high'
        ALERT_OVERSPEED = 'overspeed_start'
        RELEVANT_ALERT_TYPES = [ALERT_LOW, ALERT_MEDIUM, ALERT_HIGH, ALERT_OVERSPEED]

        driver_event_summary = EventSummary.objects.exclude(user=None).filter(type__in=RELEVANT_ALERT_TYPES).select_related(
                "device", "car", "booking", "key", "user"
            ).order_by('user__email').values('user__id', 'user__email').annotate(
                low_total=count_by_field("type", ALERT_LOW),
                # low_total=Count("type", filter=Q(type="low")),
                medium_total=count_by_field("type", ALERT_MEDIUM),
                high_total=count_by_field("type", ALERT_HIGH),
                overspeed_total=count_by_field("type", ALERT_OVERSPEED),
                total_alerts=Count('pk')
        )
        return driver_event_summary


class AllDriversEventSummaryViewSet(APIView):
    def get(self, request):
        user_id = self.request.query_params.get('user_id', None)

        driver_event_summary = get_driver_event_summary(user_id=user_id)

        required_keys = ['low_total', 'medium_total', 'high_total', 'overspeed_total', 'total_alerts']
        driver_event_summary_total = calculate_total(required_keys, driver_event_summary)

        return Response(driver_event_summary_total)

class TripViewSet(viewsets.ModelViewSet):
    queryset = TripSummary.objects.all()
    serializer_class = TripSummarySerializer
    http_method_names = ['get']
    # permission_classes = [IsAuthenticated]

class CarSummaryViewSet(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        car_summary_output = TripSummary.objects.exclude(user=None).filter(parent_trip__isnull=True).select_related(
                "device", "car", "booking", "key", "user"
            ).order_by("car__pk").values("car__pk", "car__registration_number").annotate(
                total=Count("trip_id"),
                total_mileage=meters_to_miles(Sum("mileage"))
        )
        return Response(car_summary_output)

class DriverMileageSummaryViewSet(APIView):
    def get(self, request):
        driver_summary_output = TripSummary.objects.exclude(user=None).filter(parent_trip__isnull=True).select_related(
                "device", "car", "booking", "key", "user"
            ).order_by("user__id").values("user__id", "user__email", "user__pk").annotate(
                total=Count("trip_id"),
                total_mileage=meters_to_miles(Sum("mileage"))
        )
        return Response(driver_summary_output)

class TotalMileageSummaryByTime(APIView):
    def get(self, request):
        car_summary_output = TripSummary.objects.exclude(user=None).filter(parent_trip__isnull=True).select_related(
                "device", "car", "booking", "key", "user"
            ).order_by("car__pk").annotate(
                total=Count("trip_id"),
                total_mileage=meters_to_miles(Sum("mileage"))
        )
        required_keys = ["total", "total_mileage"]
        trip_summary_total = calculate_total(required_keys, car_summary_output)
        summary_by_hour = generate_by_time_period(car_summary_output, 'hour', starting_index=0)
        summary_by_weekday = generate_by_time_period(car_summary_output, 'week_day', starting_index=0)
        results = {}
        results["trip_summary_total"] = trip_summary_total
        results["summary_by_hour"] = summary_by_hour
        results["summary_by_weekday"] = summary_by_weekday
        return Response(results)

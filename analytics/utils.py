from decimal import Decimal
from django.db.models.query import QuerySet
from django.db.models.functions import ExtractWeekDay, ExtractHour
from django.db.models import Count, Case, When, Sum
from .models import EventSummary, TripSummary
from .constants import ALERT_HIGH, ALERT_LOW, ALERT_MEDIUM, ALERT_OVERSPEED, RELEVANT_ALERT_TYPES


def meters_to_miles(val):
    return (val / 1000) * Decimal(0.621371)

def count_by_field(field, value):
    kwargs = {field: value}
    return Count(Case(When(**kwargs, then=1)))

def calculate_total(required_keys, queryset):
    if not isinstance(required_keys, list):
        raise TypeError(f"'required_keys' must be a list, got {type(required_keys)} instead")
    if not isinstance(queryset, QuerySet):
        raise TypeError(f"'queryset' must be a dictionary, got {type(queryset)} instead")
    total = {}
    for key in required_keys:
        total[key] = sum(getattr(d, key, 0) for d in queryset)
    return total

def generate_by_time_period(qs, period, starting_index):
    if period == 'week_day':
        extract_func = ExtractWeekDay
    elif period == 'hour':
        extract_func = ExtractHour
    else:
        return

    summary_over_time_period = list(
        qs.filter(
            child_trips__isnull=True
        ).exclude(user=None).select_related(
            "car", "booking", "key", "user"
        ).annotate(
            time_period=extract_func("start")
        ).order_by("time_period").values("time_period").annotate(
            total_mileage=meters_to_miles(Sum("mileage"))
        ).filter(time_period__gte=starting_index)
    )

    if period == 'hour' and len(summary_over_time_period) < 24:
        covered_hours = [d['time_period'] for d in summary_over_time_period]
        missing_hours = set(range(24)).difference(covered_hours)

        for hour in missing_hours:
            summary_over_time_period.insert(hour, {'time_period': hour, 'total_mileage': 0})

    summary_over_time_period_output = summary_over_time_period

    return summary_over_time_period_output

def get_driver_event_summary(user_id=None):
    base_query = EventSummary.objects.exclude(user=None).filter(
        type__in=RELEVANT_ALERT_TYPES
    ).select_related(
        "car", "booking", "key", "user"
    ).annotate(
        low_alerts=count_by_field("type", ALERT_LOW),
        medium_alerts=count_by_field("type", ALERT_MEDIUM),
        high_alerts=count_by_field("type", ALERT_HIGH),
        overspeed_alerts=count_by_field("type", ALERT_OVERSPEED),
        total_alerts=Count('pk')
    )

    if user_id is not None:
        base_query = base_query.filter(user__id=user_id)

    return base_query

def get_trip_mileage_summary():
    tripsummary = TripSummary.objects.exclude(user=None).filter(parent_trip__isnull=True).select_related(
                "car", "booking", "key", "user"
            ).order_by("car__pk").values("car__pk", "car__registration_number").annotate(
                total=Count("trip_id"),
                total_mileage=meters_to_miles(Sum("mileage"))
        )
    return tripsummary

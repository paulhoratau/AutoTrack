from decimal import Decimal
from django.db.models.query import QuerySet
from django.db.models.functions import ExtractWeekDay, ExtractHour
from django.db.models import Count, Case, When, Sum
from .models import EventSummary

ALERT_LOW = 'low'
ALERT_MEDIUM = 'medium'
ALERT_HIGH = 'high'
ALERT_OVERSPEED = 'overspeed_start'
RELEVANT_ALERT_TYPES = [ALERT_LOW, ALERT_MEDIUM, ALERT_HIGH, ALERT_OVERSPEED]

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
    """
    Generates an aggregated time-based summary of the Trip queryset passed in. For example, if
    you pass in a period of "week", it will sum up the total_mileage over each day of the week
    for the queryset given.

    :param qs: Queryset of Trip objects
    :param period: hour, week_day or day
    :param starting_index:
    :return:

    When period='week':

    [{'time_period': 1, 'total_mileage': 34},
        {'time_period': 2, 'total_mileage': 96},
        {'time_period': 3, 'total_mileage': 124},
        {'time_period': 4, 'total_mileage': 131},
        {'time_period': 5, 'total_mileage': 199},
        {'time_period': 6, 'total_mileage': 216},
        {'time_period': 7, 'total_mileage': 41}]
    """

    # TODO #3: Complete the rest of this filter to produce the output
    #  above where param period="week"
    if period == 'week_day':
        extract_func = ExtractWeekDay
    elif period == 'hour':
        extract_func = ExtractHour
    else:
        return

    summary_over_time_period = list(
        qs.filter(
            # Graph is time-based so we want to ignore parent Trips
            child_trips__isnull=True
        ).exclude(user=None).select_related(
            "device", "car", "booking", "key", "user"
        ).annotate(
            time_period=extract_func("start")
        ).order_by("time_period").values("time_period").annotate(
            total_mileage=meters_to_miles(Sum("mileage"))
        ).filter(time_period__gte=starting_index)
    )


    """
    This next block will take the data above and normalise it so that for the time period
    given, every possible slot has a value - filling in zeros where necessary - so it
    can be used in the graph on the Trip Summaries page.
    """

    # TODO #4: Remove the line below and modify the array from above so
    #  that the output where param period="hour" looks correct
    if period == 'hour' and len(summary_over_time_period) < 24:
        covered_hours = [d['time_period'] for d in summary_over_time_period]
        missing_hours = set(range(24)).difference(covered_hours)

        for hour in missing_hours:
            summary_over_time_period.insert(hour, {'time_period': hour, 'total_mileage': 0})

    summary_over_time_period_output = summary_over_time_period

    return summary_over_time_period_output

def get_driver_event_summary(user_id=None):
    """
    Returns a queryset for EventSummary with optional filtering by user_id.
    """
    base_query = EventSummary.objects.exclude(user=None).filter(
        type__in=RELEVANT_ALERT_TYPES
    ).select_related(
        "device", "car", "booking", "key", "user"
    ).annotate(
        low_total=count_by_field("type", ALERT_LOW),
        medium_total=count_by_field("type", ALERT_MEDIUM),
        high_total=count_by_field("type", ALERT_HIGH),
        overspeed_total=count_by_field("type", ALERT_OVERSPEED),
        total_alerts=Count('pk')
    )

    if user_id is not None:
        base_query = base_query.filter(user__id=user_id)

    return base_query

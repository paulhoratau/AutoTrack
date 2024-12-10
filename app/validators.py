from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from app.models import Booking

def validate_time_overlap(start_time, end_time, car, instance=None):

    if start_time >= end_time:
        raise ValidationError({
            "detail": _("Start time must be before end time.")
        })

    overlap_query = Q(start_time__lt=end_time, end_time__gt=start_time, car=car)
    if instance:
        overlap_query &= ~Q(pk=instance.pk)
    if Booking.objects.filter(overlap_query).exists():
        raise ValidationError({
            "detail": _("The booking overlaps with an existing booking for the selected car.")
        })

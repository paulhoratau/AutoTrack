from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .constants import VEHICLE_MANUFACTURERS, ENGINE_TYPES, KEY_STATUSES, \
    KEY_OPERATIONS, CURRENT_TYPES, EVENT_TYPES
from model_utils.models import TimeStampedModel

# Create your models here.
class TimeStampedFieldsModel(TimeStampedModel):
    """
    Mixin that adds date_added and date_updated to a Model.
    """

    class Meta:
        abstract = True

    def fields(self, fieldlist=None):
        if fieldlist:
            fieldlist = [self._meta.get_field(f) for f in fieldlist]
        else:
            fieldlist = (self._meta.fields + self._meta.many_to_many)
        fields = []
        for f in fieldlist:
            get_choice = 'get_%s_display' % f.name
            if hasattr(self, get_choice):
                value = getattr(self, get_choice)()
            elif isinstance(f, models.ManyToManyField):
                value_list = []
                for v in getattr(self, f.name).all():
                    value_list.append(str(v))
                value = ', '.join(value_list)
            else:
                try:
                    value = getattr(self, f.name)
                except User.DoesNotExist:
                    value = None

            if f.editable and value and f.name not in ('id', 'user_ptr'):
                fields.append(
                    {
                        'label': f.verbose_name,
                        'name': f.name,
                        'value': value,
                    }
                )

class Car(TimeStampedFieldsModel):
    model = models.ForeignKey("CarModel", related_name="cars", on_delete=models.CASCADE)
    year = models.IntegerField(default = 0)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    registration_number = models.CharField(max_length=10)
    location = models.ForeignKey("Location", related_name="cars", verbose_name="current location", on_delete=models.CASCADE)


class CarRepair(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    body = models.TextField(blank=False)
    created_by = models.ForeignKey('auth.User', related_name='car_repairs', on_delete=models.CASCADE)
    car = models.ForeignKey(Car, related_name='repairs', on_delete=models.CASCADE)


class CarReminder(models.Model):
    car = models.ForeignKey('Car', related_name='reminders', on_delete=models.CASCADE)
    itp = models.TextField(blank=False)
    itp_date = models.DateTimeField()
    road_tax = models.TextField(blank=False)
    road_tax_date = models.DateTimeField()
    insurance = models.TextField(blank=False)
    insurance_date = models.DateTimeField()




class Booking(TimeStampedFieldsModel):
    created_by = models.ForeignKey('auth.User', related_name='booking', on_delete=models.CASCADE)
    start_location = models.ForeignKey("Location", related_name="bookings_starting", verbose_name="Pick up location", on_delete=models.CASCADE)
    end_location = models.ForeignKey("Location", related_name="bookings_ending", verbose_name="Drop-off location", on_delete=models.CASCADE)
    start_time = models.DateTimeField(db_index=True)
    end_time = models.DateTimeField(db_index=True)
    car = models.ForeignKey('Car', related_name='booking', on_delete=models.CASCADE)


class CarModel(TimeStampedFieldsModel):
    brand = models.CharField(max_length=12, choices=VEHICLE_MANUFACTURERS, default="BMW")
    model = models.CharField(max_length=20)
    year = models.PositiveIntegerField(default="2020")
    engine_type = models.CharField(max_length=8, choices=ENGINE_TYPES, default=ENGINE_TYPES.electric)
    engine = models.PositiveIntegerField(default="1396")
    current_type = models.CharField(max_length=2, choices=CURRENT_TYPES, blank=True, null=True)
    registration_number = models.CharField(max_length=10)


class Key(TimeStampedFieldsModel):
    keycore_id = models.AutoField(primary_key=True, blank=True)
    user = models.ForeignKey('auth.User', related_name='keys', on_delete=models.CASCADE)
    booking = models.ForeignKey("Booking", related_name="keys", on_delete=models.CASCADE)
    is_put_back = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    latest_operation = models.CharField(max_length=7, choices=KEY_OPERATIONS, editable=False)
    latest_status = models.CharField(max_length=9, choices=KEY_STATUSES, editable=False,)


class KeyHistory(models.Model):
    key = models.ForeignKey("Key", related_name="history", on_delete=models.CASCADE)
    operation = models.CharField(max_length=7, choices=KEY_OPERATIONS)
    status = models.CharField(max_length=9, choices=KEY_STATUSES)
    created = models.DateTimeField(auto_now_add=True)



class Location(TimeStampedFieldsModel):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255,)
    city = models.CharField(max_length=255, verbose_name="Town / City")
    county = models.CharField(max_length=50)
    postcode = models.CharField(max_length=10)

class IdentityMixin(models.Model):
    device = models.ForeignKey(
        "Device",
        related_name='%(class)ss',
        on_delete=models.CASCADE
    )
    car = models.ForeignKey(
        "Car",
        related_name='%(class)ss',
        on_delete=models.CASCADE
    )
    booking = models.ForeignKey(
        "Booking",
        on_delete=models.SET_NULL,
        null=True,
        related_name='%(class)ss',
    )
    key = models.ForeignKey(
        "Key",
        on_delete=models.SET_NULL,
        null=True,
        related_name='%(class)ss',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='%(class)ss',
    )

    class Meta:
        abstract = True


class Event(IdentityMixin, TimeStampedFieldsModel):
    event_id = models.CharField(
        primary_key=True,
        max_length=100,
        editable=False,
    )
    timestamp = models.DateTimeField()
    type = models.CharField(
        max_length=20,
        choices=EVENT_TYPES
    )

    def __str__(self):
        return self.event_id

    class Meta:
        ordering = ['-timestamp']


class Trip(IdentityMixin, TimeStampedFieldsModel):
    trip_id = models.CharField(
        primary_key=True,
        max_length=100,
        editable=False,
    )
    parent_trip = models.ForeignKey(
        "self",
        null=True,
        related_name='child_trips',
        on_delete=models.CASCADE
    )
    start = models.DateTimeField()
    stop = models.DateTimeField()
    mileage = models.IntegerField(
        help_text="Stored in METRES as that's what the API provides",
    )
    state = models.CharField(
        max_length=100
    )

    class Meta:
        ordering = ['-start']

    def __str__(self):
        return self.trip_id

    @property
    def timestamp(self):
        return self.start

class Device(TimeStampedFieldsModel):
    serial = models.CharField(
        primary_key=True,
        max_length=50,
        editable=False,
    )
    project_id = models.CharField(
        max_length=50
    )
    license_plate = models.CharField(
        max_length=50
    )
    zone = models.CharField(
        max_length=50
    )
    car = models.ForeignKey(
        Car,
        null=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        ordering = ['serial']

    def __str__(self):
        return self.serial

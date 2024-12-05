from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .constants import VEHICLE_MANUFACTURERS, ENGINE_TYPES, KEY_STATUSES, \
    KEY_OPERATIONS, CURRENT_TYPES


# Create your models here.
class Car(models.Model):
    model = models.CharField(max_length=100, blank=True, default='')
    vin = models.CharField(max_length=17, unique=True)
    year = models.IntegerField()
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    registration_number = models.CharField(max_length=10)

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




class Booking(models.Model):
    created_by = models.ForeignKey('auth.User', related_name='booking', on_delete=models.CASCADE)
    start_location = models.ForeignKey("Location", related_name="bookings_starting", verbose_name="Pick up location", on_delete=models.CASCADE)
    end_location = models.ForeignKey("Location", related_name="bookings_ending", verbose_name="Drop-off location", on_delete=models.CASCADE)
    start_time = models.DateTimeField(db_index=True)
    end_time = models.DateTimeField(db_index=True)
    car = models.ForeignKey('Car', related_name='booking', on_delete=models.CASCADE)


class CarModel(models.Model):
    brand = models.CharField(max_length=12, choices=VEHICLE_MANUFACTURERS, default="BMW")
    model = models.CharField(max_length=20)
    year = models.PositiveIntegerField(default="2020")
    engine_type = models.CharField(max_length=8, choices=ENGINE_TYPES, default=ENGINE_TYPES.electric)
    engine = models.PositiveIntegerField(default="1396")
    current_type = models.CharField(max_length=2, choices=CURRENT_TYPES, blank=True, null=True)
    registration_number = models.CharField(max_length=10)


class Key(models.Model):
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



class Location(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255,)
    city = models.CharField(max_length=255, verbose_name="Town / City")
    county = models.CharField(max_length=50)
    postcode = models.CharField(max_length=10)

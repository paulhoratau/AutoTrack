from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Car(models.Model):
    model = models.CharField(max_length=100, blank=True, default='')
    vin = models.CharField(max_length=17, unique=True)
    year = models.IntegerField()
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

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

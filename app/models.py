from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Car(models.Model):
    model = models.CharField(max_length=100, blank=True, default='')
    vin = models.CharField(max_length=17, unique=True)
    year = models.IntegerField()
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

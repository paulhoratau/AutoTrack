from django.conf import settings
from django.db import models
from app.models import Event, Trip

class EventSummary(Event):
    class Meta:
        proxy = True
        verbose_name = 'event summary'
        verbose_name_plural = 'event summaries'


class TripSummary(Trip):
    class Meta:
        proxy = True
        verbose_name = 'trip summary'
        verbose_name_plural = 'trip summaries'

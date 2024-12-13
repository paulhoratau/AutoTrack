from django.urls import path
from . import views

urlpatterns = [
    path('events/', views.EventViewSet.as_view({'get': 'list'}), name='event-list'),
    path('trips/', views.TripViewSet.as_view({'get': 'list'}), name='trip-list'),
    path('analytics/driver_event_summary', views.DriverEventSummaryViewSet.as_view({'get': 'list'}), name="driver-event-summary"),
    path('analytics/alldrivers_event_summary', views.AllDriversEventSummaryViewSet.as_view(), name="all-drivers-event-summary"),
    path('analytics/car_summary', views.CarSummaryViewSet.as_view(), name="car-summary"),
    path('analytics/driver_mileage_summary', views.DriverMileageSummaryViewSet.as_view(), name="driver-mileage-summary"),
    path('analytics/total_mileage_summary_by_time', views.TotalMileageSummaryByTime.as_view(), name="total-mileage-summary-by-time")
]

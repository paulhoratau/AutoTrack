from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from . import views

urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('register/', views.CreateUserView.as_view(), name='register'),

    path('cars/', views.CarList.as_view(), name='car_list'),
    path('cars/create/', views.CarCreate.as_view(), name='car_create'),
    path('cars/<int:pk>/', views.CarDetail.as_view(), name='car_detail'),

    path('repairs/', views.CarRepairList.as_view(), name='car-repair-list'),
    path('repairs/<int:pk>/', views.CarRepairDetail.as_view(), name='car-repair-detail'),

    path('car_reminders/', views.CarReminderListCreate.as_view(), name='car_reminder_create'),
    path('car_reminders/<int:pk>/', views.CarReminderDetail.as_view(), name='car_reminder_detail'),

    #Bookings

    path('bookings/', views.BookingListCreateView.as_view(), name='booking-list-create'),
    path('bookings/<int:pk>/', views.BookingDetailView.as_view(), name='booking-detail'),

    path('carmodels/', views.CarModelListCreateView.as_view(), name='carmodel-list-create'),
    path('carmodels/<int:pk>/', views.CarModelDetailView.as_view(), name='carmodel-detail'),

    path('keys/', views.KeyListCreateView.as_view(), name='key-list-create'),
    path('keys/<int:pk>/', views.KeyDetailView.as_view(), name='key-detail'),

    path('keyhistories/', views.KeyHistoryListCreateView.as_view(), name='keyhistory-list-create'),
    path('keyhistories/<int:pk>/', views.KeyHistoryDetailView.as_view(), name='keyhistory-detail'),

    path('locations/', views.LocationListCreateView.as_view(), name='location-list-create'),
    path('locations/<int:pk>/', views.LocationDetailView.as_view(), name='location-detail'),

    path('contract', views.ContractCreate.as_view(), name='contract-create'),
    path('contract/<int:pk>', views.ContractDetail.as_view(), name='contract-create'),
    path('contract/sign/<int:pk>/', views.SignContract.as_view(), name='sign-contract'),

    path('generate_pdf', views.GenerateContractPDFView.as_view(), name='generate-pdf'),

    path('create_driver', views.DriverListCreateView.as_view(), name="create-driver"),
    path('driver/<int:pk>', views.DriverDetailView.as_view(), name="driver")
]

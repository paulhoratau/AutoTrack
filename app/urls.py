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
]

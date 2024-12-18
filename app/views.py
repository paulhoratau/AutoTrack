from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Car, CarRepair, CarReminder, Booking, CarModel, Key, KeyHistory, Location, Contract
from .serializers import CarSerializer, UserSerializer, CarRepairSerializer, CarReminderSerializer, BookingSerializer, CarModelSerializer, KeySerializer, KeyHistorySerializer, LocationSerializer, ContractSerializer, DriverSerializer
from .permissions import IsAdminUserWithMessage, IsAuthenticatedWithMessage
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.views import APIView
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from .models import Contract, Booking, Driver
from rest_framework.generics import RetrieveUpdateAPIView



class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class CarCreate(generics.CreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticatedWithMessage]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data['detail'] = "Car has been successfully added!"
        return response



class CarList(generics.ListAPIView):
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticatedWithMessage]


    def get_queryset(self):
        return Car.objects.filter(owner=self.request.user)

class CarDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticatedWithMessage]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(
            {"detail": "Car has been successfully updated!"},
            status=status.HTTP_200_OK
        )


class CarRepairList(generics.ListCreateAPIView):
    queryset = CarRepair.objects.all()
    serializer_class = CarRepairSerializer
    permission_classes = [IsAuthenticatedWithMessage]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data['detail'] = "Your repairing detail has been successfully added!"
        return response


    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class CarRepairDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CarRepair.objects.all()
    serializer_class = CarRepairSerializer
    permission_classes = [IsAuthenticatedWithMessage]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(
            {"detail": "Your repair has been successfully updated!"},
            status=status.HTTP_200_OK
        )

class CarReminderListCreate(generics.ListCreateAPIView):
    queryset = CarReminder.objects.all()
    serializer_class = CarReminderSerializer
    permission_classes = [IsAuthenticatedWithMessage]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data['detail'] = "Your reminder has been successfully added!"
        return response

class CarReminderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CarReminder.objects.all()
    serializer_class = CarReminderSerializer
    permission_classes = [IsAuthenticatedWithMessage]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(
            {"detail": "Reminder model has been successfully updated!"},
            status=status.HTTP_200_OK
        )


class BookingListCreateView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticatedWithMessage]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data['detail'] = "Booking has been successfully added!"
        return response

class BookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticatedWithMessage]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"detail": "Booking has been successfully deleted!"},
            status=status.HTTP_204_NO_CONTENT
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(
            {"detail": "Booking has been successfully updated!"},
            status=status.HTTP_200_OK
        )


class CarModelListCreateView(generics.ListCreateAPIView):
    queryset = CarModel.objects.all()
    serializer_class = CarModelSerializer
    permission_classes = [IsAuthenticatedWithMessage, IsAdminUserWithMessage]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data['detail'] = "Your car model has been successfully added!"
        return response

class CarModelDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CarModel.objects.all()
    serializer_class = CarModelSerializer
    permission_classes = [IsAuthenticatedWithMessage, IsAdminUserWithMessage]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"detail": "Car model has been successfully deleted!"},
            status=status.HTTP_204_NO_CONTENT
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(
            {"detail": "Car model has been successfully updated!"},
            status=status.HTTP_200_OK
        )
class KeyListCreateView(generics.ListCreateAPIView):
    queryset = Key.objects.all()
    serializer_class = KeySerializer
    permission_classes = [IsAuthenticatedWithMessage]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data['detail'] = "Key has been successfully added!"
        return response

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class KeyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Key.objects.all()
    serializer_class = KeySerializer
    permission_classes = [IsAuthenticatedWithMessage]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"detail": "The key has been successfully deleted!"},
            status=status.HTTP_204_NO_CONTENT
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(
            {"detail": "Key has been successfully updated!"},
            status=status.HTTP_200_OK
        )

class KeyHistoryListCreateView(generics.ListCreateAPIView):
    queryset = KeyHistory.objects.all()
    serializer_class = KeyHistorySerializer
    permission_classes = [IsAuthenticatedWithMessage, IsAdminUserWithMessage]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class KeyHistoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = KeyHistory.objects.all()
    serializer_class = KeyHistorySerializer
    permission_classes = [IsAuthenticatedWithMessage, IsAdminUserWithMessage]

class LocationListCreateView(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticatedWithMessage, IsAdminUserWithMessage]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data['detail'] = "Location has been successfully added!"
        return response


class LocationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticatedWithMessage, IsAdminUserWithMessage]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"detail": "Location has been successfully deleted!"},
            status=status.HTTP_204_NO_CONTENT
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(
            {"detail": "Location has been successfully updated!"},
            status=status.HTTP_200_OK
        )

class ContractCreate(generics.ListCreateAPIView):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticatedWithMessage, IsAdminUserWithMessage]

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data['detail'] = "Contract has been successfully created!"
        return response


class ContractDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticatedWithMessage, IsAdminUserWithMessage]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(
            {"detail": "Your contract has been successfully updated!"},
            status=status.HTTP_200_OK
        )


class GenerateContractPDFView(APIView):
    def get(self, request, *args, **kwargs):
        contract_id = request.query_params.get('contract_id')

        contract = get_object_or_404(Contract, pk=contract_id)
        driver = contract.driver_id
        booking = contract.booking

        response = HttpResponse(content_type='application/pdf')

        p = canvas.Canvas(response, pagesize=letter)
        width, height = letter

        p.setFont("Helvetica-Bold", 16)
        p.drawString(72, height - 72, "Contract Details")
        p.setFont("Helvetica", 12)
        p.drawString(72, height - 100, f"Contract ID: {contract.id}")
        p.drawString(72, height - 120, f"Signed: {'Yes' if contract.signed else 'No'}")
        p.drawString(72, height - 140, f"Date: {contract.date.strftime('%Y-%m-%d %H:%M:%S')}")

        p.setFont("Helvetica-Bold", 16)
        p.drawString(72, height - 180, "Booking Details")
        p.setFont("Helvetica", 12)
        p.drawString(72, height - 200, f"Car: {booking.car.model or 'N/A'}")
        p.drawString(72, height - 220, f"Contract created by: {booking.created_by or 'N/A'}")
        p.drawString(72, height - 240, f"Starts: {booking.start_time.strftime('%Y-%m-%d') if booking.start_time else 'N/A'}")
        p.drawString(72, height - 260, f"Ends: {booking.end_time.strftime('%Y-%m-%d') if booking.end_time else 'N/A'}")

        p.setFont("Helvetica-Bold", 16)
        p.drawString(72, height - 300, "Driver Details")
        p.setFont("Helvetica", 12)

        p.drawString(72, height - 320, f"First name: {driver.first_name or 'N/A'}")
        p.drawString(72, height - 340, f"Last name: {driver.last_name or 'N/A'}")
        p.drawString(72, height - 360, f"Age: {driver.age or 'N/A'}")
        p.drawString(72, height - 380, f"Email: {driver.email or 'N/A'}")
        p.drawString(72, height - 400, f"Phone number: {driver.phone or 'N/A'}")
        p.drawString(72, height - 420, f"Passport id: {driver.passport_id or 'N/A'}")

        p.showPage()
        p.save()

        return response



class DriverListCreateView(generics.ListCreateAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [IsAuthenticatedWithMessage, IsAdminUserWithMessage]

class DriverDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [IsAuthenticatedWithMessage, IsAdminUserWithMessage]

class SignContract(generics.UpdateAPIView):
    queryset = Contract.objects.filter(signed=False)
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticatedWithMessage]

    def perform_update(self, serializer):
        serializer.save(signed=True)

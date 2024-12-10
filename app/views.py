from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Car, CarRepair, CarReminder, Booking, CarModel, Key, KeyHistory, Location
from .serializers import CarSerializer, UserSerializer, CarRepairSerializer, CarReminderSerializer, BookingSerializer, CarModelSerializer, KeySerializer, KeyHistorySerializer, LocationSerializer
from .permissions import IsAdminUserWithMessage, IsAuthenticatedWithMessage

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

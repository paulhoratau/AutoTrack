from rest_framework import generics, permissions
from .models import Car, CarRepair, CarReminder
from .serializers import CarSerializer, UserSerializer, CarRepairSerializer, CarReminderSerializer

class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class CarCreate(generics.CreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CarList(generics.ListAPIView):
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Car.objects.filter(owner=self.request.user)

class CarDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticated]

class CarRepairList(generics.ListCreateAPIView):
    queryset = CarRepair.objects.all()
    serializer_class = CarRepairSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class CarRepairDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CarRepair.objects.all()
    serializer_class = CarRepairSerializer
    permission_classes = [permissions.IsAuthenticated]

class CarReminderListCreate(generics.ListCreateAPIView):
    queryset = CarReminder.objects.all()
    serializer_class = CarReminderSerializer
    permission_classes = [permissions.IsAuthenticated]

class CarReminderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CarReminder.objects.all()
    serializer_class = CarReminderSerializer
    permission_classes = [permissions.IsAuthenticated]

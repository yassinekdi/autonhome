from rest_framework import generics
from .models import Sensor, Measure, CalendarEvent
from .serializers import SensorSerializer, MeasureSerializer, CalendarEventSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework import permissions
from .permissions import IsUserOrAdmin

from django.shortcuts import get_object_or_404

class SensorList(generics.ListCreateAPIView):
    serializer_class = SensorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Sensor.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SensorDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SensorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Sensor.objects.filter(user=self.request.user)


class MeasureList(generics.ListCreateAPIView):
    serializer_class = MeasureSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Measure.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        user_id = self.request.data['user']
        user = User.objects.get(id=user_id)
        serializer.save(user=user)




class MeasureDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MeasureSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Measure.objects.filter(user=self.request.user)


class CalendarEventList(generics.ListCreateAPIView):
    serializer_class = CalendarEventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CalendarEvent.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CalendarEventDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CalendarEventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CalendarEvent.objects.filter(user=self.request.user)


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.request.method == 'GET':
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsUserOrAdmin]

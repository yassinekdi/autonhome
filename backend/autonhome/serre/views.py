from rest_framework import generics
from .models import Sensor, Measure, CalendarEvent
from .serializers import SensorSerializer, MeasureSerializer, CalendarEventSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework import permissions

class SensorList(generics.ListCreateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = [IsAuthenticated]

class SensorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = [IsAuthenticated]

class MeasureList(generics.ListCreateAPIView):
    queryset = Measure.objects.all()
    serializer_class = MeasureSerializer
    permission_classes = [IsAuthenticated]

class MeasureDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Measure.objects.all()
    serializer_class = MeasureSerializer
    permission_classes = [IsAuthenticated]

class CalendarEventList(generics.ListCreateAPIView):
    queryset = CalendarEvent.objects.all()
    serializer_class = CalendarEventSerializer
    permission_classes = [IsAuthenticated]

class CalendarEventDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CalendarEvent.objects.all()
    serializer_class = CalendarEventSerializer
    permission_classes = [IsAuthenticated]

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  # Anybody can create a user

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

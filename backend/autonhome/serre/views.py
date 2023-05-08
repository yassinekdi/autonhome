from django.shortcuts import render
from rest_framework import generics
from .models import Sensor, Measure, CalendarEvent
from .serializers import SensorSerializer, MeasureSerializer, CalendarEventSerializer
from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse
from django.views import View
from rest_framework.permissions import IsAuthenticated

class SensorList(generics.ListCreateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    # permission_classes = [IsAuthenticated]

class SensorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    # permission_classes = [IsAuthenticated]

class MeasureList(generics.ListCreateAPIView):
    queryset = Measure.objects.all()
    serializer_class = MeasureSerializer
    # permission_classes = [IsAuthenticated]

class MeasureDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Measure.objects.all()
    serializer_class = MeasureSerializer
    # permission_classes = [IsAuthenticated]

class CalendarEventList(generics.ListCreateAPIView):
    queryset = CalendarEvent.objects.all()
    serializer_class = CalendarEventSerializer
    # permission_classes = [IsAuthenticated]

class CalendarEventDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CalendarEvent.objects.all()
    serializer_class = CalendarEventSerializer
    # permission_classes = [IsAuthenticated]

class LoginView(View):
    def post(self, request):
        # Authenticate the user using the provided credentials
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Log the user in and return a JSON response with the user's ID
            login(request, user)
            return JsonResponse({'user_id': user.id})
        else:
            # If authentication fails, show an error message
            return JsonResponse({'error_message': "Nom d'utilisateur ou mot de passe incorrect"}, status=401)

class LogoutView(View):
    def get(self, request):
        # Log the user out and return a JSON response
        logout(request)
        return JsonResponse({'message': 'Déconnecté avec succès'})

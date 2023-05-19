from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Sensor, Measure, CalendarEvent, SensorType

class SensorTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorType
        fields = '__all__'

class SensorSerializer(serializers.ModelSerializer):
    types = SensorTypeSerializer(many=True, read_only=True)
    class Meta:
        model = Sensor
        fields = '__all__'

class MeasureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measure
        fields = '__all__'

class CalendarEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarEvent
        fields = '__all__'



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

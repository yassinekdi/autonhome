from rest_framework import serializers
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

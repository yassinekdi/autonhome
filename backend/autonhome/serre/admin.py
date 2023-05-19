from django.contrib import admin
from .models import SensorType, Sensor, Measure

admin.site.register(SensorType)
admin.site.register(Sensor)
admin.site.register(Measure)

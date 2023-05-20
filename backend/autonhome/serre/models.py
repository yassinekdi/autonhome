from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class SensorType(models.Model):
    TYPE_CHOICES = (
        ('Temperature', 'Temperature'),
        ('Humidity', 'Humidity'),
        ('Luminosity', 'Luminosity'),
        # Add other sensor types if necessary
    )
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, null=True)

    def __str__(self):
        return self.type

class Sensor(models.Model):
    SECTION_CHOICES = (
        ('Air', 'Air'),
        ('Soil', 'Soil'),
        ('Water', 'Water'),
    )

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    types = models.ManyToManyField(SensorType)
    section = models.CharField(max_length=15, choices=SECTION_CHOICES)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

class Measure(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    value = models.FloatField()
    timestamp = models.DateTimeField(default=timezone.now)
    section = models.CharField(max_length=15, choices=Sensor.SECTION_CHOICES, null=True)
    label = models.CharField(max_length=100, null=True)
    unit = models.CharField(max_length=20, null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    class Meta:
        unique_together = (('sensor', 'value', 'timestamp', 'label', 'unit'),)

    def __str__(self):
        return f"{self.sensor.name} - {self.value} - {self.timestamp}"

    def save(self, *args, **kwargs):
        self.section = self.sensor.section
        super().save(*args, **kwargs)



class CalendarEvent(models.Model):
    EVENT_TYPE_CHOICES = (
        ('SEM', 'Semis'),
        ('REP', 'Repiquage'),
        ('REC', 'Récolte'),
        # Add other event types if necessary
    )

    event_type = models.CharField(max_length=5, choices=EVENT_TYPE_CHOICES)
    date = models.DateField()
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.title} - {self.date}"

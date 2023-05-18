from django.db import models
from django.utils import timezone


class Sensor(models.Model):
    TYPE_CHOICES = (
        ('Temperature', 'Temperature'),
        ('Humidity', 'Humidity'),
        ('Luminosity', 'Luminosity'),
        # Add other sensor types if necessary
    )
    SECTION_CHOICES = (
        ('Air', 'Air'),
        ('Soil', 'Soil'),
        ('Water', 'Water'),
        # Add other sensor types if necessary
    )

    sensor_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    section = models.CharField(max_length=15, choices=SECTION_CHOICES)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Measure(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    value = models.FloatField()
    timestamp = models.DateTimeField(default=timezone.now)
    section = models.CharField(max_length=15, choices=Sensor.SECTION_CHOICES, blank=True)

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

    def __str__(self):
        return f"{self.title} - {self.date}"

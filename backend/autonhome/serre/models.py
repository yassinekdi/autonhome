from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from pathlib import Path
from syncs.user_sync import UserSync
from .constants import SECTIONS_CHOICE,SENSOR_TYPE_CHOICES
import os

class SensorType(models.Model):
    
    type = models.CharField(max_length=20, choices=SENSOR_TYPE_CHOICES, null=True)

    def __str__(self):
        return self.type

class Sensor(models.Model):
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    types = models.ManyToManyField(SensorType)
    section = models.CharField(max_length=15, choices=SECTIONS_CHOICE)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

class Measure(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    value = models.FloatField()
    timestamp = models.DateTimeField(default=timezone.now)
    section = models.CharField(max_length=15, choices=SECTIONS_CHOICE, null=True)
    label = models.CharField(max_length=100, null=True)
    unit = models.CharField(max_length=20, null=True, blank=True)
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


def user_post_save(sender, instance, created, **kwargs):
    main_dir = Path(__file__).parents[3]
    user_dir = os.path.join(main_dir, 'backend','users')
    if created:
        # create the user directory
        user_dir = os.path.join(user_dir, str(instance.id))
        os.makedirs(user_dir, exist_ok=True)

        #TODO: run the user_sync script
        user_sync = UserSync(user_dir, os.path.join(main_dir, 'SensorsToCopy'))
        user_sync.sync()

        

# connect the function to the User model's post_save signal
models.signals.post_save.connect(user_post_save, sender=User)

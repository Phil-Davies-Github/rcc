from django import forms
from django.db import models

# Create your models here.
# Basic Test Models

# Basic Test classes to enable race updates and race points calculations
class Event(models.Model):
    name = models.CharField(max_length=80)
    order = models.FloatField(default=999)

    def __str__(self):
       return str(self.name)

class Yacht(models.Model):   # Define physical characteristics of a yacht
    sail_number = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(max_length=80, null=True)
    
    def __str__(self):
        return f"{self.sail_number} - {self.name}"
    
class Handicap(models.Model): # Define the dynamic characteristics of the yacht
    yacht = models.ForeignKey(Yacht, on_delete=models.CASCADE)
    current_handicap = models.SmallIntegerField()

    def __str__(self):
        return f"{self.yacht.sail_number} - {self.yacht.name}"

class ItemModel(models.Model):
    name = models.CharField(max_length=100)
    handicap = models.IntegerField()
    elapsed_time_input = models.CharField(max_length=20)
    elapsed_time_seconds = models.IntegerField(null=True, blank=True)
    elapsed_time_minutes = models.FloatField(null=True, blank=True)

class RaceDetail(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)
    race_name = models.CharField(max_length = 100)
    number = models.SmallIntegerField()

# Intermediate Classes
class EventEntry(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    yacht = models.OneToOneField(Yacht, on_delete=models.CASCADE)
    date = models.DateField()

    class Meta:
        verbose_name_plural = "Event entries"
    
    def __str__(self):
        return f"{self.event.name} - {self.yacht.sail_number} - {self.yacht.name}"

class EventRaceResult(models.Model):
    race_detail = models.ForeignKey(RaceDetail, on_delete=models.CASCADE)
    event_entry = models.ForeignKey(EventEntry, on_delete=models.CASCADE)

    field1 = models.DurationField(null=True)
    field2 = models.BooleanField(null=True)
    field3 = models.DurationField(null=True)
    field4 = models.SmallIntegerField(null=True)
from django import forms
from django.db import models

# Create your models here.
# Basic Test Models

# Basic Test classes to enable race updates and race points calculations
class Event(models.Model):
    name = models.CharField(max_length=80)
    order = models.FloatField(default=999)
    date = models.DateField(null=True)

    def __str__(self):
       return f"{self.date.year} - {self.name}"

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

class Race(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length = 100)
    order = models.SmallIntegerField()

    def __str__(self):
        return f"{self.event.name}[{self.event.date.year}] - {self.name}"

# Intermediate Classes
class EventEntry(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    yacht = models.OneToOneField(Yacht, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Event entries"
    
    def __str__(self):
        return f"{self.event.name}[{self.event.date.year}] - ({self.yacht.sail_number}) {self.yacht.name}"

class EventRace(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    event_entry = models.ForeignKey(EventEntry, on_delete=models.CASCADE)
    # Race data
    handicap_applied = models.IntegerField(null=True)
    elapsed_time = models.CharField(max_length=20)
    elapsed_time_seconds = models.IntegerField(null=True, blank=True)
    elapsed_time_minutes = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.event_entry.event.name}[{self.event_entry.event.date.year}] {self.race.name} - ({self.event_entry.yacht.sail_number}) {self.event_entry.yacht.name}"
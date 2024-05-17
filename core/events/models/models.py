from django.db import models
from django.urls import reverse
from yachts.models import Yacht

# Create your models here.
class RecurringEvent(models.Model):
    name = models.CharField(max_length=80)
    order = models.FloatField(default=999)
    duration = models.PositiveSmallIntegerField()
    type = models.CharField(
        max_length=5,
        choices=[
            ('Open', 'Open'),
            ('Club', 'Club'),
        ], 
        default = 'Open',
        null = False
    )
    location = models.CharField(
        max_length=5, 
        choices=[
            ('River', 'River'),
            ('Broad', 'Broad'),
        ], 
        default = 'River',
        null = False
    )
    code = models.CharField(max_length=20)
    no_races = models.PositiveSmallIntegerField()
    no_discards = models.PositiveSmallIntegerField()
    is_sabrina = models.BooleanField()
    sabrina_order = models.FloatField(blank=True, null=True)
    is_snowbird = models.BooleanField()
    snowbird_order = models.FloatField(blank=True, null=True)
    #race = models.ForeignKey('Race', on_delete=models.CASCADE, null=True)

    def __str__(self):
       return str(self.name)

class Year(models.Model):
    recurring_events = models.ForeignKey(RecurringEvent,on_delete=models.CASCADE, null=True)
    year = models.PositiveSmallIntegerField(primary_key=True, unique=True)

    def __str__(self):
       return str(self.year)

class Event(models.Model):
    recurring_event = models.ForeignKey(RecurringEvent, on_delete=models.CASCADE)
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    date = models.DateField()
    #event_entry = models.ForeignKey(Yacht, on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = ('recurring_event', 'year')

    def update_details(self, new_date, **kwargs):
        # Update the event details for a specific year
        self.date = new_date
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save()

    def get_absolute_url(self):
        # Generate a URL based on a pattern named 'event_entries' in the events workspace
        # using the 'year' attribute of the current instance
        # We are here
        return reverse('events:events', kwargs={'year': self.year})
        
    def __str__(self):
       return f"{self.year} - {self.recurring_event.name}"
    
class Race(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length = 100)
    splits = models.SmallIntegerField()
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
    elapsed_time_minutes = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=3)
    corrected_time_seconds = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places= 3)
    corrected_time_minutes = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places= 3)
    
    def __str__(self):
        return f"{self.event_entry.event.name}[{self.event_entry.event.date.year}] {self.race.name} - ({self.event_entry.yacht.sail_number}) {self.event_entry.yacht.name}"

# A self contained Model which contains only the published results
class EventResult(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    position = models.SmallIntegerField(null=True, blank=True)
    points = models.SmallIntegerField(null=True, blank=True)
    margin = models.FloatField()
    handicap_change_to_win = models.FloatField()
    penalty = models.BooleanField()
    event_race = models.ForeignKey(EventRace, on_delete=models.CASCADE)

class EventOverallRaceResult(models.Model):
    event_result = models.ForeignKey(EventRace, on_delete=models.CASCADE)
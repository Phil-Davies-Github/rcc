from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

class Yacht(models.Model):   
    sail_number = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(max_length=80, null=True)
    owners = models.CharField(max_length=80, null=True)
    helm = models.CharField(max_length=80, null=True)
    flag = models.CharField(max_length=80, blank=True)
    updated_by = models.CharField(max_length=80, null=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.sail_number} - {self.name}"
    
class Handicap(models.Model):
    sail_number = models.PositiveSmallIntegerField(primary_key = True)
    current_handicap = models.SmallIntegerField()
    current_status = models.CharField(
        max_length=12, 
        choices=[
            ('Provisional','Provisional'),
            ('Ratified', 'Ratified'),
            ('None', 'None'),
        ], 
        default='Provisional'
    )
    reason_for_change = models.CharField(max_length=80)
    amended_by = models.CharField(max_length=80)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.yacht.name} ({self.current_handicap})"
    
class HistoricalHandicap(models.Model):
    yacht = models.ForeignKey(Yacht, on_delete=models.CASCADE, related_name='historical_handicap')
    historical_handicap = models.SmallIntegerField(null=True)
    reason_for_change = models.CharField(max_length=80, null=True)
    amended_by = models.CharField(max_length=80, null=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.yacht} - {self.historical_handicap}"

# Triggered just before a handicap change so tha the last handicap value can be stored
@receiver(pre_save, sender=Handicap)
def pre_save_handicap(sender, instance, **kwargs):
    try:
        original_instance = Handicap.objects.get(pk=instance.pk)
    except Handicap.DoesNotExist:
        return  # The original instance doesn't exist, so it's likely a new object
    # Check if the instance has already been saved and store the last status and handicap (i.e., it's an update)
    if instance.pk:
        instance.last_handicap = original_instance.current_handicap    
        instance.last_status = original_instance.status

# Triggered after the handicap has been updated and writes to the historical log
          
@receiver(post_save, sender=Handicap)
def create_historical_handicap(sender, instance, **kwargs):
    # Your post-save logic 
   
    # Check if the instance has already been saved (i.e., it's an update)
    if instance.pk:
        # Check if the current_handicap or status has changed and save to the history log
        if instance.current_handicap != instance.last_handicap or instance.status != instance.last_status:
            historical_handicap = HistoricalHandicap.objects.create(
                yacht_id=instance.yacht.sail_number,
                historical_handicap=instance.last_handicap,
                reason_for_change=instance.reason_for_change,
                amended_by = instance.amended_by,
            )
            
# Connect the signals
post_save.connect(create_historical_handicap, sender=Handicap)
    
class Analytics(models.Model):
    yacht = models.ForeignKey(Yacht, on_delete=models.CASCADE, related_name='analytics')
    wins_this_year = models.SmallIntegerField(("wins"))
    places_this_year = models.SmallIntegerField(("places"))
    races_this_year = models.SmallIntegerField(("no races this year"))
    average_hCap_change_to_win = models.SmallIntegerField(("ave hcw"))
    standard_deviation_hCap_change_to_win = models.SmallIntegerField(("std dev hcw"))
    average_position = models.SmallIntegerField(("average position"))

    def __str__(self):
        return f"Analytics for {self.yacht.sail_number}"
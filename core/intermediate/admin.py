from django.contrib import admin
from . import models 

# Define ModelAdminForms
class EventRaceAdmin(admin.ModelAdmin):
    exclude = (
        'event_entry', 
        'race', 
        'yacht',
        'elapsed_time_seconds',
        'elapsed_time_minutes',
    )


# Register your models here.
admin.site.register(models.ItemModel)
admin.site.register(models.Race)
admin.site.register(models.Event)
admin.site.register(models.EventEntry)
admin.site.register(models.EventRace, EventRaceAdmin)
admin.site.register(models.Yacht)
admin.site.register(models.Handicap)
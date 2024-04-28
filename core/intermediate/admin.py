from django.contrib import admin
from . import models 
# Register your models here.
admin.site.register(models.ItemModel)
admin.site.register(models.RaceDetail)
admin.site.register(models.Event)
admin.site.register(models.EventEntry)
admin.site.register(models.EventRaceResult)
admin.site.register(models.Yacht)
admin.site.register(models.Handicap)
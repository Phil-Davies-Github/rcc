from django import forms
from django.db import models

# Create your models here.
# Basic Test Model
class ItemModel(models.Model):
    name = models.CharField(max_length=100)
    handicap = models.IntegerField()
    elapsed_time_seconds = models.IntegerField(null=True, blank=True)
    elapsed_time_minutes = models.FloatField(null=True, blank=True)

class Object1(models.Model):
    name = models.CharField(max_length = 100)
    number = models.SmallIntegerField()

class Object2(models.Model):
    name = models.CharField(max_length = 100)
    date = models.DateField()

class Intermediate(models.Model):
    object1 = models.ForeignKey(Object1, on_delete=models.CASCADE)
    object2 = models.ForeignKey(Object2, on_delete=models.CASCADE)

    field1 = models.DurationField(null=True)
    field2 = models.BooleanField(null=True)
    field3 = models.DurationField(null=True)
    field4 = models.SmallIntegerField(null=True)
from django import forms
from django.db import models

# Extend the models.Field class to include 
class DurationField(models.Field):
    description = "Duration in seconds"

    def from_db_value(self, value, expression, connection):
        if value is None:
            return None
        return float(value)

    def to_python(self, value):
        if value is None:
            return None
        return float(value)

    def get_prep_value(self, value):
        if value is None:
            return None
        return float(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return str(value)

    def validate(self, value, model_instance):
        if value is None:
            return
        if not isinstance(value, float) or value < 0:
            raise forms.ValidationError("Duration must be a positive float value.")

# Create your models here.
# Basic Test Model
class ItemModel(models.Model):
    name = models.CharField(max_length=100)
    estimated_price = models.IntegerField()
    elapsed_time_seconds = models.DurationField()

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
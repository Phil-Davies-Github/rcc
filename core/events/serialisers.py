from rest_framework import serializers
from events.models import Year, Event

# Allow Django Model to be Converted to JSON
class YearSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Year
        fields = ('year', 'recurring_events_id')

class EventSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('year', 'recurring_event')
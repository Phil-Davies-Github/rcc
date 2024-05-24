from django.contrib import admin
from django import forms
from events.models import models
from yachts.models import Yacht, Handicap

class EventsAdminArea(admin.AdminSite):
    site_header='Events Admin Area'

# Reference the class
events_admin = EventsAdminArea(name='EventsAdmin')

events_admin.site_header = "RCC Events Admin Area"
events_admin.site_title = "RCC Events Admin Portal"
events_admin.index_title = "Welcome to RCC Events Portal"

# Define a custom form for the RecurringEvent model
class RecurringEventForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        print("Initializing Recurring Event Form")
        super(RecurringEventForm, self).__init__(*args, **kwargs)

    class Meta:
        model = models.RecurringEvent
        fields = '__all__'

class RecurringEventFormAdmin(admin.ModelAdmin):
    form = RecurringEventForm
    list_display = ['name', 'duration', 'type', 'location',]
    #inlines = [RacesInRecurringEventInline]

class EventEntryForm(forms.ModelForm):
    class Meta:
        model = models.EventEntry
        fields = '__all__'

class EventEntryFormAdmin(admin.ModelAdmin):
    form = EventEntryForm

class YearForm(forms.ModelForm):
    
    '''
    recurring_event = forms.ModelChoiceField(
        queryset=RecurringEvent.objects.all(),
        widget=forms.Select(attrs={'disabled': 'disabled'}),
    )
    '''

    def __init__(self, *args, **kwargs):
        print("Initializing YearForm")
        super(YearForm, self).__init__(*args, **kwargs)
        #print("Queryset:", self.fields['recurring_event'].queryset)

    class Meta:
        model = models.Year
        fields = ['year', ]
        exclude = ['recurring_event', ]

class YearFormAdmin(admin.ModelAdmin):
    form = YearForm
    list_display = ['year']
    # inlines = [EventInline]
    #inlines = [EventInline]

    #def recurring_event_name(self, obj):
    #    if obj.recurring_event:
    #       return obj.recurring_event.name
    #    return None
    # recurring_event_name.short_description = 'Recurring Event'
    
    #def get_form(self, request, obj=None, **kwargs):
    #    form = super().get_form(request, obj, **kwargs)
    #   form.fields['recurring_event'].queryset = RecurringEvent.objects.all()
    #    return form
    
    def __init__(self, *args, **kwargs):
        print("Initializing YearFormAdmin")
        super().__init__(*args, **kwargs)
       
    
# auto fill the year field
    '''
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'recurring_event':
            # If the recurring_event is set in the URL (editing from within a Year), use that value
            if 'recurring_event__id__exact' in request.GET:
                kwargs['initial'] = {'recurring_event': request.GET['recurring_event__id__exact']}
            else:
                # If not, you might want to set a default value here or leave it blank
                kwargs['initial'] = {'recurring_event': None}
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
                
    '''            
class EventAdmin(admin.ModelAdmin):
    fields = ['year', 'date', 'recurring_event']

class EventRaceAdmin(admin.ModelAdmin):
    exclude = (
        'event_entry', 
        'race', 
        'yacht',
        'elapsed_time_seconds',
        'elapsed_time_minutes',
    )

# Register your models here.
events_admin.register(models.Race)
events_admin.register(models.RecurringEvent, RecurringEventFormAdmin)
events_admin.register(models.Year, YearFormAdmin)
events_admin.register(models.Event, EventAdmin)
events_admin.register(models.EventEntry, EventEntryFormAdmin)
events_admin.register(models.EventRace, EventRaceAdmin)
events_admin.register(models.EventOverallRaceResult)
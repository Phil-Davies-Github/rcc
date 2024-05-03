#from django.forms import ModelForm, BaseInlineFormSet, modelformset_factory
from django.shortcuts import get_object_or_404
from . import models
from django import forms

# Define ModelForm and fields to interact with
class ItemModelForm(forms.ModelForm):
    class Meta:
        model = models.ItemModel
        fields = ['name', 'handicap', 'elapsed_time_input']

    # Validation logic, Input conversion and additional fields
    # These fields are not automatically saved to the database. 
    # They are part of the forms cleaned data but not the model instance
    # add to the model date in the view
    def clean_elapsed_time_input(self):
        elapsed_time_string = self.cleaned_data.get('elapsed_time_input')

        if elapsed_time_string is None:
            return None
        
        if '.' in elapsed_time_string:
            elapsed_seconds = int(float(elapsed_time_string) * 60)
            self.cleaned_data['elapsed_time_seconds'] = elapsed_seconds
            self.cleaned_data['elapsed_time_minutes'] = float(elapsed_time_string)
            return elapsed_time_string

        if ':' in elapsed_time_string:
            # Try parsing as hours:minutes:seconds
            try:
                parts = elapsed_time_string.split(":")
                hours = int(parts[0])
                minutes = int(parts[1])
                seconds = int(parts[2])
                total_seconds = hours * 3600 + minutes * 60 + seconds
                self.cleaned_data['elapsed_time_seconds'] = total_seconds
                self.cleaned_data['elapsed_time_minutes'] = total_seconds / 60
                return elapsed_time_string
            except (ValueError, IndexError):
                raise forms.ValidationError("Invalid duration format. Please check the format i.e. hh:mm:ss or mm.mm or ss")

        # if not hh:mm:ss or float assume seconds   
        elapsed_seconds = int(elapsed_time_string)
        self.cleaned_data['elapsed_time_seconds'] = elapsed_seconds
        self.cleaned_data['elapsed_time_minutes'] = (float(elapsed_time_string) / 60)
        return elapsed_time_string
        
# Straightforward formset which handles multiple instances automatically generating a formset based on model
# and form class
# Define EventRace Intermediate model and fields to interact with
class EventRaceModelForm(forms.ModelForm):
        
    class Meta:
        model = models.EventRace
        fields = ['elapsed_time', 'handicap_applied', ]
    '''
    # Initialise the Current Handicap field
    def __init__(self, *args, **kwargs):
        super(EventRaceModelForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            # Get the entered yacht
            yacht = self.instance.event_entry.yacht
            # Get the current handicap instance and initialise the handicap applied field
            handicap = models.Handicap.objects.get(yacht=yacht)
            self.fields['handicap'].initial = handicap.current_handicap
    '''

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Assuming object1_id is a ForeignKey field in Intermediate model
        if self.cleaned_data.get('object1_name'):
            object1 = get_object_or_404(models.Race, name=self.cleaned_data['object1_name'])
            instance.object1 = object1
        if commit:
            instance.save()
        return instance

    # Called as part of is_valid(). Validation logic, Elapsed time input conversion to seconds and minutes.
    # The additional form fields are not automatically saved to the database. 
    # They are become part of the forms cleaned data but not the model instance
    # These fields are added to the model data in the view
    def clean_elapsed_time(self):
        elapsed_time_string = self.cleaned_data.get('elapsed_time')

        if elapsed_time_string is None:
            return None
        
        if '.' in elapsed_time_string:
            elapsed_seconds = int(float(elapsed_time_string) * 60)
            self.cleaned_data['elapsed_time_seconds'] = elapsed_seconds
            self.cleaned_data['elapsed_time_minutes'] = float(elapsed_time_string)
            return elapsed_time_string

        if ':' in elapsed_time_string:
            # Try parsing as hours:minutes:seconds
            try:
                parts = elapsed_time_string.split(":")
                hours = int(parts[0])
                minutes = int(parts[1])
                seconds = int(parts[2])
                total_seconds = hours * 3600 + minutes * 60 + seconds
                self.cleaned_data['elapsed_time_seconds'] = total_seconds
                self.cleaned_data['elapsed_time_minutes'] = total_seconds / 60
                return elapsed_time_string
            except (ValueError, IndexError):
                raise forms.ValidationError("Invalid duration format. Please check the format i.e. hh:mm:ss or mm.mm or ss")

        # if not hh:mm:ss or float assume seconds   
        elapsed_seconds = int(elapsed_time_string)
        self.cleaned_data['elapsed_time_seconds'] = elapsed_seconds
        self.cleaned_data['elapsed_time_minutes'] = (float(elapsed_time_string) / 60)
        return elapsed_time_string

'''
# Used for customisation of base classes
class IntermediateFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class IntermediateForm(ModelForm):

    def __init__(self, *args, **kwargs):
        object2_id = kwargs.pop('object2_id', None)
        super().__init__(*args, **kwargs)
        if object2_id: # check object2_id was passed as an argument
            object1_instances = Object1.objects.filter(intermediate__object2_id=object2_id)
            self.fields['field_to_update'].queryset = object1_instances

    class Meta:
        model = Intermediate
        fields=['field1', 'field2', 'field3', 'field4',]

# Allows interaction with multiple instance. 
# Inlineformset factory assumes that the parent model include the primary key to itself

'''
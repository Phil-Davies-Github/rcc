#from django.forms import ModelForm, BaseInlineFormSet, modelformset_factory
from django.shortcuts import get_object_or_404
from .models import Intermediate, Object1, ItemModel
from django import forms

# Define ModelForm and fields to interact with
class ItemModelForm(forms.ModelForm):
    elapsed_time = forms.CharField(max_length=20, required=False)

    class Meta:
        model = ItemModel
        fields = ['name', 'estimated_price', 'elapsed_time']

    # Validation logic, Input conversion and additional fields
    # These fields are not automatically saved to the database. 
    # They are part of the forms cleaned data but not the model instance
    def clean_elapsed_time(self):
        elapsed_time = self.cleaned_data.get('elapsed_time')
        if elapsed_time is None:
            return None
        
        if isinstance(elapsed_time, int):
            self.cleaned_data['elapsed_time_seconds'] = elapsed_time
            self.cleaned_data['elapsed_time_minutes'] = elapsed_time / 60
            return elapsed_time
        
        if isinstance(elapsed_time, float):
            self.cleaned_data['elapsed_time_seconds'] = elapsed_time * 60
            self.cleaned_data['elapsed_time_minutes'] = elapsed_time
            return elapsed_time
        
        # Try parsing as hours:minutes:seconds
        try:
            parts = elapsed_time.split(":")
            hours = int(parts[0])
            minutes = int(parts[1])
            seconds = int(parts[2])
            total_seconds = hours * 3600 + minutes * 60 + seconds
            self.cleaned_data['elapsed_time_seconds'] = total_seconds
            self.cleaned_data['elapsed_time_minutes'] = total_seconds / 60
            return total_seconds
        except (ValueError, IndexError):
            raise forms.ValidationError("Invalid duration format. Please use hh:mm:ss or seconds as a integer.")


# Straightforward formset which handles multiple instances automatically generating a formset based on model
# and form class
class IntermediateModelForm(forms.ModelForm):
    # define fields from related objects
    object1_name = forms.CharField(
        max_length=100, 
        required=False,
        # widget allows customisation of how the form field is rendered
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
    )
    class Meta:
        model = Intermediate
        fields = ['object2', 'field1', 'field2', 'field3', 'field4']

    def __init__(self, *args, **kwargs):
        super(IntermediateModelForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['object1_name'].initial = self.instance.object1.name

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Assuming object1_id is a ForeignKey field in Intermediate model
        if self.cleaned_data.get('object1_name'):
            object1 = get_object_or_404(Object1, name=self.cleaned_data['object1_name'])
            instance.object1 = object1
        if commit:
            instance.save()
        return instance

IntermediateFormSet = forms.modelformset_factory(
    Intermediate,  
    form=IntermediateModelForm,
    extra=0,
    can_delete=False
)


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
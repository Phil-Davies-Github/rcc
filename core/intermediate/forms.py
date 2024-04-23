#from django.forms import ModelForm, BaseInlineFormSet, modelformset_factory
from django.shortcuts import get_object_or_404
from .models import Intermediate, Object1, ItemModel
from django import forms

# Custom field type which accepts hh:mm:ss, int or float
class DurationField(forms.Field):
    def to_python(self, value):
        if value in [None, '', []]:
            return None

        # If it's already a float, assume it's in minutes
        if isinstance(value, float):
            return value * 60

        # If it's already a int, assume it's in seconds
        if isinstance(value, int):
            return value

        # Try parsing as hours:minutes:seconds
        try:
            parts = value.split(":")
            hours = int(parts[0])
            minutes = int(parts[1])
            seconds = int(parts[2])
            total_seconds = hours * 3600 + minutes * 60 + seconds
            return total_seconds
        except (ValueError, IndexError):
            raise forms.ValidationError("Invalid duration format. Please use hh:mm:ss or seconds as a integer.")

# Create a custom form which 
class ItemModelForm(forms.ModelForm):
    #elapsed_time_input = DurationField()
    elapsed_time_input = forms.CharField(max_length=10)

    class Meta:
        model = ItemModel
        fields = ['name', 'estimated_price', 'elapsed_time_input']

    '''
    def clean_elapsed_time_input(self):
        seconds = self.cleaned_data.get('elapsed_time_input')
        if seconds is None:
            return None
    '''  

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
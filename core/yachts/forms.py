from django import forms
from .models import Handicap

class HandicapAdminForm(forms.ModelForm):
    class Meta:
        model = Handicap
        fields = '__all__'
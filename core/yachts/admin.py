from django.contrib import admin
from django import forms

from .models import Yacht, Handicap

class YachtsAdminArea(admin.AdminSite):
    site_header='Yachts Admin Area'

# Instantiate Events Object here.
yachts_admin_site = YachtsAdminArea(name='YachtsAdmin')

class YachtAdmin(admin.ModelAdmin):
    pass

    def get_form(self, request, obj=None, **kwargs):
        # Override the get_form method to customize the form - needs a form to work with 
        print(f"Yacht Admin Form Override")
        form = super().get_form(request, obj, **kwargs)
        return form

# create custom form
class HandicapForm(forms.ModelForm):
    previous_handicap = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    previous_reason = forms.CharField(required=False, max_length=80, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    previous_updated_by = forms.CharField(required=False, max_length=80, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    previous_status = forms.CharField(required=False, max_length=80, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    date_amended = forms.DateField(required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    last_handicap = forms.IntegerField(required=False, widget=forms.HiddenInput())
    last_status = forms.CharField(required=False, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        print("Initializing Handicap Form")
        super(HandicapForm, self).__init__(*args, **kwargs)

        # Access the instance using self.instance
        if self.instance.pk:
            # Populate the Previous Handicap Information
            print(f"Instance : {self.instance}")
            # Initialise the hidden field
            self.fields['last_handicap'].initial = self.instance.current_handicap
            '''   
            # Get the previous historical handicap record
            previous_handicap = self.instance.yacht.historical_handicap.order_by('-updated').exclude(id=self.instance.id).first()
            # Fetch and populate previous handicap information
            
            if previous_handicap:
                # Update form field with the previous handicap data
                self.fields['previous_handicap'].initial = previous_handicap.historical_handicap
                self.fields['previous_reason'].initial = previous_handicap.reason_for_change
                self.fields['previous_updated_by'].initial = previous_handicap.amended_by
                self.fields['date_amended'].initial = previous_handicap.updated

            print(f"Previous Handicap {previous_handicap}")
            '''

    class Meta:
        model = Handicap
        fields = ['current_handicap', 'reason_for_change', 'amended_by',]
        exclude = ['yacht', ]

class HandicapAdmin(admin.ModelAdmin):
    #form = HandicapAdminForm
    list_display = ['yacht', 'current_handicap', 'status', 'reason_for_change', 'amended_by', 'updated']
    
    '''
    def get_form(self, request, obj=None, **kwargs):
        # Override the get_form method to customize the form
        print(f"Handicap Admin Form Override")
        form = super().get_form(request, obj, **kwargs)

        # Fetch the previous handicap and set it as the initial value for the form
        if obj and obj.pk:  # Check if the instance is being edited (obj is not None and has a primary key)
            print(f"Handicap Admin - Object {obj}")
            last_historical_handicap = obj.yacht.historical_handicap.order_by('-updated').exclude(id=obj.id).first()
            print(f"Previous Handicap {last_historical_handicap}")
            if last_historical_handicap:
                pass
                # Set the initial value for the previous_handicap field
                #form.base_fields['previous_handicap'].initial = last_historical_handicap.handicap
        return form
    '''
       
yachts_admin_site.register(Yacht, YachtAdmin)
yachts_admin_site.register(Handicap, HandicapAdmin)
from typing import Any
from django.shortcuts import redirect, render
from django.views.generic import FormView, ListView, TemplateView
from intermediate.models import EventRace, Race, ItemModel
from .forms import EventRaceModelForm, ItemModelForm
from django.forms import modelformset_factory, formset_factory
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.contrib import messages
from .models import EventEntry, Handicap
from django.urls import reverse

# Test Object View
class DeleteItem(FormView):
    pass

class ItemUpdateView(FormView):
    # specify what needs to be used
    template_name = 'formset_view.html'
    # Each form is associate with an instance of the ItemModel
    # Only modelformsets have a save method so create a modelformset
    form_class = modelformset_factory(
        ItemModel,
        form = ItemModelForm,
        extra = 0
    )
    success_url = 'success'

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        queryset = ItemModel.objects.all() 
        context['item_formset'] = self.form_class(queryset=queryset)
        return context
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        formset = self.form_class(request.POST, request.FILES)
        print(formset)
        if formset.is_valid():
            # add the additional form fields to the database by adding to the corresponding model instance
            for form in formset:
                # get the instance to update from the model
                instance = form.instance
                if instance.pk: # if instance has a primary key
                    instance.elapsed_time_seconds = form.cleaned_data['elapsed_time_seconds'] 
                    instance.elapsed_time_minutes = form.cleaned_data['elapsed_time_minutes'] 
                    instance.corrected_time_seconds = form.cleaned_data['corrected_time_seconds']
                    instance.save()
                
            messages.success(request, "Item Saved to database")
            # This creates a new formset instance with only the saved instances
            # formset = self.form_class(queryset=ItemModel.objects.filter(id__in=[instance.id for instance in instances]))
            # To obtain all instances of the item object, fetch the data from the database        
            all_instances = ItemModel.objects.all()
            formset = self.form_class(queryset=all_instances)
            
            # Redirect user to url after save
            return render(request, self.template_name, {'item_formset': formset})
        else: 
            return self.render_to_response({'item_formset': formset})


    def form_valid(self, form):
        
        return super().form_valid(form)
    
    # Rerender the form with error
    def form_invalid(self, form) -> HttpResponse:
        return self.render_to_response(self.get_context_data(form=form))  

# Create your views here.
class Index(TemplateView):
    template_name='index.html'

class IntermediateListView(ListView):
    model=EventRace
    template_name='intermediate_list.html'

    # Override the get_context_data so that relevant data can be retrieved from then database
    def get_context_data(self, **kwargs):
        related_object2_instances = []
        seen_ids = set()

        context = super().get_context_data(**kwargs)
       
        # Retrieve only unique items in queryset and pass to the context
        unique_object2 = EventRace.objects.values('object2_id').distinct()
        context['distinct_object2_instances'] = unique_object2
        
        # Only append the distinct instance of related_object2
        # by iterating through the Intermediate Object looking for the first instance of each distinct object2 
        for intermediate_obj in EventRace.objects.all():
            object2_id = intermediate_obj.object2_id
            if object2_id not in seen_ids:
                seen_ids.add(object2_id)
                # Add to query
                related_object2_instances.append(intermediate_obj.event_entries)
        # Pass related Object2 instances to context
        context['related_object2_instances'] = related_object2_instances
        return context

class EventRaceResultsListView(ListView):
    model=EventRace
    template_name='list_event_race_results.html'

    # Determine positions
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        #kwargs['race_id'] = self.kwargs['race_id']
        self.race_id = self.kwargs['race_id']
        # Get the Event Race Detail for the specific instance
        event_race = EventRace.objects.get(id = self.race_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        race_id = self.kwargs['race_id']
        # arrange fastest first then assign a position and margin
        yacht_result = EventRace.objects.filter(race_id = race_id).order_by('corrected_time_minutes')
        results = []
        for position, yacht in enumerate(yacht_result, start=1):
            # Calculate the handicap margin between yachts up the last yacht
            if position < yacht_result.count():               
                handicap_margin = round((yacht_result[position].corrected_time_seconds/yacht.elapsed_time_seconds -1) * 100-yacht.handicap_applied, 2)
            else:
                handicap_margin = 0
            
            # Calculate Handicap Change to Win
            if position == 1:
                handicap_change_to_win = 0
            else:
                # Take the time of the wining yacht and calcuate the handicap required to match this time
                handicap_change_to_win = round(((yacht_result[0].corrected_time_seconds/yacht.elapsed_time_seconds-1) * 100 - yacht.handicap_applied) * -1, 1)
            
            results.append({
                'yacht' : yacht,
                'position' : position,
                'margin' : handicap_margin,
                'hcw' : handicap_change_to_win
            })   
        
        context['results'] = results
        return context

class EventRaceUpdateView(FormView):
    # class scoped varaiables
    race_id = 0
    # specify rendering template
    template_name='update_event_race_results_form.html'
    # Each form is associate with an instance of EventRaceResults
    form_class = modelformset_factory(
        EventRace,
        form = EventRaceModelForm,
        extra = 0
    )
    success_url='/success/'

    # if a yacht is entered for an event, override the init method so that 
    # populate the race table with the competitors
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        #kwargs['race_id'] = self.kwargs['race_id']
        self.race_id = self.kwargs['race_id']
        # Get the RaceDetail for the specific instance
        event_race = Race.objects.get(id = self.race_id)
        # Retrieve all event entries associated with the race 
        entries = EventEntry.objects.filter(event_id=event_race.event_id)
        # Check each entry and add to the EventRace table if missing
        for entry in entries:
            # Retrieve handicap associated with the entered yacht
            yacht = entry.yacht
            # Get the handicap instance for the yacht and initialise the handicap applied field
            handicap = Handicap.objects.get(yacht=yacht)
            race_entry, created = EventRace.objects.get_or_create(
                race_id = self.race_id, 
                event_entry_id = entry.id,
                defaults={'handicap_applied': handicap.current_handicap}, 
            )

        return kwargs

    # The view needs to render the EventRaceResults fields together with the related RaceDetail and EventEntries
    # The following get_context override retrieves the querysets for the EventRaceResults and rekated RaceDetail 
    # and EventEntries

    # This binds a queryset directly, but Django typically binds 
    # formsets to a dictionary object. Typically, a data is bound in a POST or GET Request
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Extract the value of race_id from the URL parameters
        #race_id = self.kwargs.get('race_id')  
        # Extract entries from the event_race 
        queryset = EventRace.objects.filter(race_id=self.race_id)
        Formset = self.get_form_class()
        if self.request.method == 'POST':
            context['formset'] = Formset(self.request.POST, queryset=queryset)
        else:
            context['formset'] = Formset(queryset=queryset)   # data is unbound when making a GET request     
        return context
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        race_id = self.kwargs['race_id']
        formset = self.form_class(request.POST, request.FILES)

        if formset.is_valid():
            # Process Buttons
            if 'save' in request.POST:
                for form in formset:
                    if form.has_changed():
                        # get the instance
                        instance = form.instance
                        if instance.pk: # if instance has a primary key save
                            instance.elapsed_time_seconds = form.cleaned_data['elapsed_time_seconds'] 
                            instance.elapsed_time_minutes = form.cleaned_data['elapsed_time_minutes'] 
                            instance.handicap_applied = form.cleaned_data['handicap_applied'] 
                            # Calculate Corrected Time 
                            handicap_applied = form.cleaned_data.get('handicap_applied')
                            instance.corrected_time_seconds = instance.elapsed_time_seconds * (1 + float(handicap_applied)/100) 
                            instance.corrected_time_minutes = instance.corrected_time_seconds / 60
                            instance.save()
                # re-load the updated data from the database
                race_instances = EventRace.objects.filter(race_id = race_id)
                formset = self.form_class(queryset=race_instances)
                # Redirect user to url after save
                return render(request, self.template_name, {'formset': formset}) 
            elif 'results' in request.POST:
                               
                # redirect to results list view
                url = reverse('intermediate:list_event_race_results', kwargs = {'race_id': race_id})
                return HttpResponseRedirect(url)  
            
             
    # Called when form is submitted and passes validation
    def form_valid(self, form):
        form.save()
        # Redirect or show success message
        return super().form_valid(form)
    

    
    

# Function Based Views
def submit_view(request):
    initial_form_data = {
        'name': 'Rock',
        'estimated_price': 0,
    }
    if request.method=="GET":
        item_form = ItemModelForm(initial=initial_form_data)
    elif request.method=="POST":
        item_form = ItemModelForm(data=request.POST,
                                     initial=initial_form_data)
        if item_form.is_valid() and item_form.has_changed():
            name = item_form.cleaned_data['name']
            estimated_price = item_form.cleaned_data['estimated_price']
            message = f'Thanks for your submission of {name}, \
                        with an estimated price of {estimated_price}!'
            return HttpResponse(message)

    context = {
        'item_form': item_form
    }
    return render(request, 'submit.html', context)

def formset_submit_view(request):
    ItemFormSet = formset_factory(ItemModelForm, extra=2)
    item_formset = ItemFormSet()
    context = {
        'item_formset': item_formset
    }
    return render(request, 'formset_view.html', context)
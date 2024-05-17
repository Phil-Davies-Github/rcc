from typing import Any
from django.shortcuts import redirect, render
from django.views.generic import FormView, ListView, TemplateView
#from events.models import EventResult, EventRace, Race, EventEntry, Handicap
from events.models import models
from events.forms import EventRaceModelForm
from django.forms import modelformset_factory
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse

# Create your views here.
class Index(TemplateView):
    template_name='index.html'

# Event Views

class YearsListView(ListView):
    # overrides
    model = models.Year
    template_name='year_list.html'

class EventsListView(ListView):
    model = models.Event
    template_name = 'events_list.html'
    # override the get_context_data method to get the dynamic data
    
    def get_context_data(self, **kwargs):
        # get context data from the parent
        context = super().get_context_data(**kwargs)
        # extract the year attribute from the first instance
        if self.object_list.exists():
            year = self.object_list.first().year
            context['year'] = year

        return context
        
    def get_queryset(self):
        year = self.kwargs['year']
        return models.Event.objects.filter(year=year)

class EventEntryListView(ListView):
    model = models.EventEntry
    template_name = 'event_entry_list.html'
    # override get_context_data method to dynamic content i.e event name
    # object_list is an auto generated list 
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        if self.object_list.exists():
            first_entry = self.object_list.first()
            # Fetch the event name from the first instance of the queryset
            event_name = first_entry.event.recurring_event.name
            event_year = first_entry.event.year
            context['event_name'] = event_name
            context['year'] = event_year        
        return context

# Results Views
class EventResultsListView(ListView):
    model = models.EventResult
    template_name = 'event_results_list.html'

class EventRaceResultsListView(ListView):
    model=models.EventRace
    template_name='list_event_race_results_list.html'

    # Determine positions
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        #kwargs['race_id'] = self.kwargs['race_id']
        self.race_id = self.kwargs['race_id']
        # Get the Event Race Detail for the specific instance
        event_race = models.EventRace.objects.get(id = self.race_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        race_id = self.kwargs['race_id']
        # arrange fastest first then assign a position and margin
        yacht_result = models.EventRace.objects.filter(race_id = race_id).order_by('corrected_time_minutes')
        results = []
        for position, event_race in enumerate(yacht_result, start=1):
            # Calculate the handicap margin between yachts up the last yacht
            if position < yacht_result.count():               
                handicap_margin = round((yacht_result[position].corrected_time_seconds/event_race.elapsed_time_seconds -1) * 100-event_race.handicap_applied, 2)
            else:
                handicap_margin = 0
            # Calculate Handicap Change to Win
            if position == 1:
                handicap_change_to_win = 0
            else:
                # Take the time of the wining yacht and calcuate the handicap required to match this time
                handicap_change_to_win = round(((yacht_result[0].corrected_time_seconds/event_race.elapsed_time_seconds-1) * 100 - event_race.handicap_applied) * -1, 1)
            
            # Did the yacht take a penalty?
            penalty = False

            results.append({
                'event' : event_race.event_entry.event,
                'race' : event_race.race,
                'event_race' : event_race,
                'penalty' : penalty,
                'position' : position,
                'points' : position,
                'margin' : handicap_margin,
                'handicap_change_to_win' : handicap_change_to_win
            })   
        # now write the results table
        for result in results:
            race_result, created = models.EventResult.objects.get_or_create(**result)
        context['results'] = results
        return context

class EventRaceUpdateView(FormView):
    # class scoped varaiables
    race_id = 0
    # specify rendering template
    template_name='event_race_results_update.html'
    # Each form is associate with an instance of EventRaceResults
    form_class = modelformset_factory(
        models.EventRace,
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
        event_race = models.Race.objects.get(id = self.race_id)
        # Retrieve all event entries associated with the race 
        entries = models.EventEntry.objects.filter(event_id=event_race.event_id)
        # Check each entry and add to the EventRace table if missing
        for entry in entries:
            # Retrieve handicap associated with the entered yacht
            yacht = entry.yacht
            # Get the handicap instance for the yacht and initialise the handicap applied field
            handicap = models.Handicap.objects.get(yacht=yacht)
            race_entry, created = models.EventRace.objects.get_or_create(
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
        queryset = models.EventRace.objects.filter(race_id=self.race_id)
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
                race_instances = models.EventRace.objects.filter(race_id = race_id)
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
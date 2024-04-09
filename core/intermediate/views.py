from django.shortcuts import render
from django.views.generic import FormView, ListView, TemplateView
from django.views.generic.detail import SingleObjectMixin
from intermediate.models import Intermediate, Object1
from .forms import IntermediateModelForm, IntermediateFormSet

# Create your views here.
class Index(TemplateView):
    template_name='index.html'

class IntermediateListView(ListView):
    model=Intermediate
    template_name='intermediate_list.html'

    # Override the get_context_data so that relevant data can be retrieved from then database

    def get_context_data(self, **kwargs):
        related_object2_instances = []
        seen_ids = set()

        context = super().get_context_data(**kwargs)
       
        # Retrieve only unique items in queryset and pass to the context
        unique_object2 = Intermediate.objects.values('object2_id').distinct()
        context['distinct_object2_instances'] = unique_object2
        
        # Only append the distinct instance of related_object2
        # by iterating through the Intermediate Object looking for the first instance of each distinct object2 
        for intermediate_obj in Intermediate.objects.all():
            object2_id = intermediate_obj.object2_id
            if object2_id not in seen_ids:
                seen_ids.add(object2_id)
                # Add to query
                related_object2_instances.append(intermediate_obj.object2)
        # Pass related Object2 instances to context
        context['related_object2_instances'] = related_object2_instances
        return context

class IntermediateUpdateView(FormView):
    model = Intermediate
    form_class = IntermediateModelForm
    template_name='update_intermediate_form.html'
    success_url='/success/'

    # The view needs to render the intermediate field together with the related object1 name
    # The following get_context override retrieves the querysets for both the intermediate instances 
    # and the object1
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Extract the value of object2_id from the URL parameters
        object2_id = self.kwargs.get('object2_id')  
        # Extract multiple instances filtered by the value of object 2 
        intermediate_queryset = Intermediate.objects.filter(object2_id=object2_id)
        # Get related object1 data
        related_object1_instances = Object1.objects.filter(id__in=intermediate_queryset.values('object1_id'))
        formset = IntermediateFormSet(queryset=intermediate_queryset)
        # populate related object1 data in each form instance
        # define the form
        '''
        form = formset.empty_form
        # iterates over pairs of elements from two iterables (formset and related_object1_instances) simultaneously
        
        for form, related_object1_instance in zip(formset, related_object1_instances):
            form.fields['object1_name'].initial = related_object1_instance.name if related_object1_instance else ""
        '''
        context['formset'] = formset
        #context['related_object1_instances'] = related_object1_instances
        return context
        
    # Called when form is submitted and passes validation
    def form_valid(self, form):
        form.save()
        # Redirect or show success message
        return super().form_valid(form)
    '''
    def post(self, request, *args, **kwargs):
        # get object we want to work with
        self.object = self.get_object(queryset=Intermediate.objects.all)
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class=None):
        return IntermediateFormSet(**self.get_form_kwargs(), instance=self.object)
    '''
   
    
    # Get keyword arguments that will be passed to the form class



    '''
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['object2_id'] = self.kwargs['object2_id']
        return kwargs

    # Called when form is submitted and passes validation
    def form_valid(self, form):
        form.save()
        # Redirect or show success message
        return super().form_valid(form)
    '''